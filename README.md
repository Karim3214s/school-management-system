# 🎓 School Management System

A full-featured **School Management System** built using Flask that enables efficient management of students, teachers, classes, subjects, and assignments with role-based access.

---

## 🚀 Features

### 🔐 Authentication System

* Secure login system
* First-time login password setup
* Forgot password with CAPTCHA verification
* Role-based access (Admin, Teacher, Student)

---

### 👨‍💼 Admin Panel

* Dashboard with statistics
* Manage Students (Add, Edit, Delete, Search)
* Manage Teachers (Add, Edit, Delete, Search)
* Manage Classes (Supports 10 A, 10 B, etc.)
* Manage Subjects
* Assign Teachers to Classes & Subjects
* Prevent duplicate teacher assignments
* View & Reply to Contact Messages
* Approve/Reject Feedbacks

---

### 👨‍🏫 Teacher Panel

* View assigned classes & subjects
* View students under their classes
* Profile management

---

### 🎓 Student Panel

* View dashboard
* Access assigned class details

---

### 💬 Communication Features

* Contact form (user → admin)
* Admin reply system (with optional email)
* Feedback system with approval workflow

---

### 🛡️ Security Features

* Password hashing using Werkzeug
* Session-based authentication
* CAPTCHA for password reset
* Input validation

---

## 🧰 Tech Stack

* **Backend:** Flask (Python)
* **Database:** SQLite (via SQLAlchemy ORM)
* **Frontend:** HTML, CSS, Bootstrap, JavaScript
* **Authentication:** Flask Sessions
* **Email Service:** Flask-Mail

---

## 📂 Project Structure

```
School_app/
│
├── models/              # Database models
├── routes/              # Application routes (admin, auth, teacher, student)
├── templates/           # HTML templates
├── static/              # CSS, JS, images
├── utils/               # Custom decorators and helpers
├── config.py            # Configuration file
├── app.py               # Main application entry point
└── requirements.txt     # Dependencies
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/karim3214s/school-management-system.git
cd school-management-system
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run Application

```bash
python app.py
```

---

### 5️⃣ Open in Browser

```text
http://127.0.0.1:5000
```

---

## 🔑 Default Admin Credentials

```
Email: admin@school.com
Password: admin123
```

---

## 📸 Screenshots (Add Later)

* Admin Dashboard
* Manage Students Page
* Assign Teachers Page
* Login & Reset Password Page

---

## 📈 Future Enhancements

* OTP-based password reset
* Role-based permissions (fine-grained)
* Attendance management system
* Marks & grading system
* File uploads for assignments
* Deployment on cloud (AWS / Render)

---

## 👤 Author

**Karim**

* GitHub: https://github.com/karim3214s
* LinkedIn: http://www.linkedin.com/in/karimulla-shaik-97a872258

---

## ⭐ Contribution

Contributions are welcome! Feel free to fork this repo and improve it.

---

## 📄 License

This project is open-source.
