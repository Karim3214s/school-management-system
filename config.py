import os

class Config:
    # =========================
    # 🔐 SECRET KEY
    # =========================
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-school-key')

    # =========================
    # 🗄️ DATABASE
    # =========================
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:K%40rim3214s@localhost:5432/school_app'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================
    # 📧 MAIL CONFIG
    # =========================
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'shaik.karim3214@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # =========================
    # 🧪 DEBUG (optional)
    # =========================
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'

    # =========================
    # pagination
    # =========================
    per_page = 5