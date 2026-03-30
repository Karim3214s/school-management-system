from flask import Flask
from config import Config
from models import db
from models.user import User
from werkzeug.security import generate_password_hash
from flask_mail import Mail

# Blueprints
from routes.common_routes import common_bp
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.teacher_routes import teacher_bp
from routes.student_routes import student_bp

mail = Mail()


def create_app():
    """Application Factory"""

    app = Flask(__name__)

    # 🔥 LOAD CONFIG (ONLY ONCE)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    mail.init_app(app)

    print("MAIL USER:", app.config['MAIL_USERNAME'])
    print("MAIL PASS:", app.config['MAIL_PASSWORD'])

    # =========================
    # 🔗 Register Blueprints
    # =========================

    # NOTE: DO NOT repeat url_prefix here (already defined in blueprint)

    app.register_blueprint(common_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(student_bp)

    # =========================
    # 🛠️ Setup DB + Seed
    # =========================
    with app.app_context():
        db.create_all()
        seed_admin()

    return app


# =========================
# 🌱 SEED ADMIN
# =========================
def seed_admin():
    admin_exists = User.query.filter_by(role='admin').first()

    if not admin_exists:
        admin = User(
            name="Admin",
            email="admin@school.com",
            password=generate_password_hash("admin123"),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("✅ Admin user created (admin@school.com / admin123)")
    else:
        print("ℹ️ Admin already exists")


# =========================
# 🚀 RUN APP
# =========================
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)