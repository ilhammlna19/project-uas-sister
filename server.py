from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
from flask_session import Session
from flask_socketio import SocketIO, emit
from models import db, Message
import pytz
from datetime import datetime
from datetime import timedelta
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'  # Tambahkan ini
Session(app)
USERS = {
    "admin": "admin",
    "user": "user"
}
app.permanent_session_lifetime = timedelta(minutes=10)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt', 'zip', 'rar', 'xls', 'xlsx', 'ppt', 'pptx'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

db.init_app(app)
socketio = SocketIO(app, async_mode='gevent')

with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Username atau password salah!")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Proteksi semua halaman utama
@app.before_request
def require_login():
    allowed_endpoints = [
        'login', 'logout', 'static', 'uploaded_file'
    ]
    # Jika endpoint None (misal favicon), biarkan lewat
    if request.endpoint is None:
        return
    # Izinkan static dan file upload tanpa login
    if (request.endpoint in allowed_endpoints or
        request.endpoint.startswith('static')):
        return
    # Jika belum login, redirect ke login
    if 'username' not in session:
        return redirect(url_for('login'))

@app.route('/')
def index():
    messages = Message.query.order_by(Message.timestamp.asc()).all()
    return render_template('index.html', messages=messages)

@app.route('/clear', methods=['POST'])
def clear_history():
    Message.query.delete()
    db.session.commit()
    socketio.emit('clear_history')  # Tambahkan baris ini
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    username = request.form.get('username', 'anonymous')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Simpan ke database
        msg = Message(
            username=username,
            content=f"Upload file: {filename}",
            timestamp=datetime.now(pytz.timezone('Asia/Jakarta')),
        )
        db.session.add(msg)
        db.session.commit()
        # Emit ke client
        socketio.emit('receive_file', {
            'username': username,
            'filename': filename,
            'url': url_for('uploaded_file', filename=filename),
            'timestamp': msg.timestamp.strftime('%d-%m-%Y %H:%M:%S')
        })
    return redirect(url_for('index'))

@app.route('/history')
def history():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('history.html', messages=messages)

@socketio.on('send_message')
def handle_send_message(data):
    username = data['username']
    content = data['content']
    wib = pytz.timezone('Asia/Jakarta')
    now = datetime.now(wib)
    msg = Message(username=username, content=content, timestamp=now)
    db.session.add(msg)
    db.session.commit()
    socketio.emit('receive_message', {
        'username': username,
        'content': content,
        'timestamp': msg.timestamp.strftime('%d-%m-%Y %H:%M:%S')
    })

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Tambahkan set untuk menyimpan sid user yang online
online_users = set()

@socketio.on('connect')
def handle_connect():
    online_users.add(request.sid)
    ip_addr = request.remote_addr
    print(f"User connected: {request.sid} (IP: {ip_addr}). Online: {len(online_users)} user(s): {list(online_users)}")

@socketio.on('disconnect')
def handle_disconnect():
    online_users.discard(request.sid)
    print(f"User disconnected: {request.sid}. Online: {len(online_users)} user(s): {list(online_users)}")

if __name__ == '__main__':
    try:
        socketio.run(app, debug=True, host='172.10.6.82', port=5000)
    except KeyboardInterrupt:
        print("\nServer stopped by user (server off)")

# konfigurasinya sama berbeda ip saja 
