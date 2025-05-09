# 🔐 OS Lock Screen Security System

A full-screen lock screen interface built using **Python's Tkinter** library, simulating a secure OS-like login system with aesthetic visuals, blurred backgrounds, user profiles, and login verification using a MySQL database.

Designed to create a real-time user login experience — visually similar to Windows lock screens with additional freeze protection after multiple failed attempts.

---

### 🌟 Features

- 🖼️ Random background wallpaper with blur effect  
- ⏰ Real-time date and time display  
- 👤 Multiple user profiles with circular avatars  
- 🔒 Secure password-based login system  
- ❌ Lockout mechanism after 5 failed attempts (15 sec freeze)  
- 🎯 Mouse pointer trap during lockout using `pyautogui`  
- 🧠 Smart foreground color based on background brightness  
- 🧵 Multi-threaded clock update  
- 🧑‍💻 MySQL-based user authentication system  

---

### ▶️ How to Run

1. Ensure all dependencies are installed (see below).
2. Place your background wallpapers in the `Wallpapers` folder.
3. Add user profile images to the `User Profiles` folder.
4. Set up your MySQL database and run the provided `.sql` file.
5. Run the Python script:

```bash
python your_script_name.py
```

---

### 🧩 Requirements

- Python 3.x
- MySQL Server
- Python Libraries:
  ```bash
  pip install pillow mysql-connector-python pyautogui
  ```

---

### 🗃️ Data Base Structure

#### 📑 Table: `users`

```sql
CREATE TABLE `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(100),
  `email` VARCHAR(100),
  `password` VARCHAR(100),
  `image` VARCHAR(100),
  PRIMARY KEY (`id`)
);
```

#### 🧪 Sample Data

```sql
INSERT INTO `users` (`username`, `email`, `password`, `image`) VALUES
('Yug Agarwal', 'yugagarwal704@gmail.com', '1234', 'yug.png'),
('Saksham Kotia', 'saksham@example.com', 'shubh@123', 'saksham.jpg'),
('Avisha Agarwal', 'avisha@gmail.com', 'secure@1', 'avisha.jpeg'),
('Rida Geelani', 'rida@gmail.com', 'alphabeta', 'rida.jpeg');

```

---

### 🗂️ Project Structure

```
📁 OS-Lock-Screen/
│
├── Wallpapers/            # Background wallpapers
├── User Profiles/         # Profile images
├── Windows-New-Logo.png   # Window icon
├── os_lock_screen.py      # Main script
├── database.sql           # SQL setup file
└── README.md              # Project README
```

---

### ⚠️ Security Warning

- ❗ Passwords are stored as **plain text** in the database for simplicity.
- 🔐 Always **hash passwords** using libraries like `bcrypt` or `argon2` in production.
- 🧪 This project is meant for **learning and demonstration purposes** only.

---

### 👨‍💻 Author

**Yug Agarwal**  
- 📧 [yugagarwal704@gmail.com](mailto:yugagarwal704@gmail.com)  
- 🔗 GitHub – [@HelloYug](https://github.com/HelloYug)
