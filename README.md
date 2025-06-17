# project-uas-sister
# SISTeR PRO APP++

Aplikasi chat real-time berbasis web dengan fitur login session, upload file, dan failover server (server utama & backup).  
Dibangun menggunakan **Flask**, **Flask-SocketIO**, dan **SQLite**.

---

## Fitur Utama

- **Login Session:** User wajib login sebelum mengakses aplikasi.
- **Chat Real-Time:** Pesan dikirim dan diterima secara langsung (Socket.IO).
- **Upload File:** Kirim file gambar, dokumen, dan lainnya.
- **History Chat:** Lihat riwayat chat dan file yang pernah dikirim.
- **Hapus History:** Admin/user dapat menghapus seluruh riwayat chat.
- **Tampilan Responsif:** Nyaman digunakan di desktop maupun mobile.

---

## Struktur Folder

```
sister_uas_fix/
│
├── server.py              # Server utama
├── server_backup.py       # Server backup
├── models.py              # Model database (SQLAlchemy)
├── lihat_db.py            # Script melihat isi database
├── requirements.txt       # Daftar dependensi Python
│
├── uploads/               # Folder file upload
│
├── templates/
│   ├── index.html         # Halaman utama chat
│   ├── login.html         # Halaman login
│   └── history.html       # Halaman riwayat chat
│
└── static/
    ├── style.css          # CSS tambahan (opsional)
    ├── notif.mp3          # Suara notifikasi
    └── img/
        ├── logoweb.png    # Logo aplikasi
        └── profile.png    # Icon user
```

---

## Cara Menjalankan

1. **Install dependensi:**
   ```
   pip install -r requirements.txt
   ```

2. **Jalankan server utama:**
   ```
   python server.py
   ```
   Atau jalankan server backup di mesin/IP berbeda:
   ```
   python server_backup.py
   ```

3. **Akses aplikasi di browser:**
   ```
   http://<ip-server>:5000/
   ```
   Contoh: `http://192.168.1.15:5000/`

4. **Login dengan akun:**
   - Username: `admin` | Password: `admin`
   - Username: `user`  | Password: `user`

---

## Catatan

- **Database:** Default menggunakan SQLite (`chat.db`). Untuk sinkronisasi penuh antar server,
- **Session:** Otomatis logout setelah 10 menit tidak aktif.

## Screenshot

![Login Page](templates/login.html)
![Cuplikan layar 2025-06-16 231837](https://github.com/user-attachments/assets/16206f60-4658-415d-8440-cb0c6e345926)

![Chat Page](templates/index.html)
![Cuplikan layar 2025-06-17 095920](https://github.com/user-attachments/assets/ef818543-4ab5-452e-9707-e07242986f47)

![History Page](templates/history.html)
![Cuplikan layar 2025-06-16 085707](https://github.com/user-attachments/assets/70ec092b-a746-4e8b-a5ac-219d9e0ee46c)
