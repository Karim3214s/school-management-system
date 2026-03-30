import email

from flask import Blueprint, flash, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# =========================
# 🔐 LOGIN
# =========================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    # If already logged in
    if 'user_id' in session:
        return redirect_based_on_role(session.get('role'))

    # =====================
    # GET → Render page
    # =====================
    if request.method == 'GET':
        return render_template('common/login.html')

    # =====================
    # POST → API (JSON)
    # =====================
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "error",
                "message": "Invalid request format"
            }), 400

        email = data.get('email').strip().lower()
        password = data.get('password')

        # Validation
        if not email or not password:
            return jsonify({
                "status": "error",
                "message": "Email and password are required"
            }), 400

        # Find user
        email = email.strip().lower()
        user = User.query.filter_by(email=email).first()

        # Check password
        if not user or not check_password_hash(user.password, password):
            return jsonify({
                "status": "error",
                "message": "Invalid email or password"
            }), 401

        # Create session
        session['user_id'] = user.id
        session['role'] = user.role
        session['name'] = user.name

        # Return JSON (IMPORTANT for frontend)
        # 🔥 FIRST LOGIN CHECK
        if user.is_first_login:
            return jsonify({
                "status": "first_login",
                "message": "Please create new password",
                "redirect": url_for('auth.create_password')
            })

        return jsonify({
            "status": "success",
            "message": "Login successful",
            "redirect": get_redirect_url(user.role)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500




# =========================
# 🔐 CREATE PASSWORD PAGE
# =========================
@auth_bp.route('/create-password')
def create_password():

    # allow both flows
    if not (session.get('user_id') or session.get('reset_mode')):
        return redirect(url_for('auth.login'))

    return render_template('common/create_password.html')


# =========================
# 🔐 SET PASSWORD API
# =========================
@auth_bp.route('/set-password', methods=['POST'])
def set_password():

    data = request.get_json()
    password = data.get("password")
    email = data.get("email")

    if not password:
        return jsonify({"status": "error", "message": "Password required"}), 400

    # 🔥 FORGOT PASSWORD FLOW
    if session.get('reset_mode'):

        if not email:
            return jsonify({"status": "error", "message": "Email required"}), 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"status": "error", "message": "Email not found"}), 404

    # 🔥 FIRST LOGIN FLOW
    else:
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({"status": "error", "message": "Unauthorized"}), 401

        user = User.query.get(user_id)

    # 🔥 UPDATE PASSWORD
    user.password = generate_password_hash(password)
    user.is_first_login = False

    db.session.commit()

    # 🔥 CLEAN SESSION
    session.pop('reset_mode', None)
    session.pop('user_id', None)

    return jsonify({
        "status": "success",
        "redirect": url_for('auth.login')
    })

# =========================
# Forgot password page 
# =========================
@auth_bp.route('/forgot-password')
def forgot_password():

    # 🔥 enable reset mode
    session['reset_mode'] = True

    return redirect(url_for('auth.create_password'))

# =========================
# 🚪 LOGOUT
# =========================
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('common.home'))


# =========================
# 🔀 REDIRECT LOGIC
# =========================
def redirect_based_on_role(role):
    return redirect(get_redirect_url(role))


def get_redirect_url(role):
    """Returns URL (used in JSON response)"""
    if role == 'admin':
        return url_for('admin.dashboard')
    elif role == 'teacher':
        return url_for('teacher.dashboard')
    elif role == 'student':
        return url_for('student.dashboard')
    return url_for('common.home')