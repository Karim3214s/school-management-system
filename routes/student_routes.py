from flask import Blueprint, render_template, session, redirect, url_for
from functools import wraps
from models.student import Student
from models.marks import Mark

student_bp = Blueprint('student', __name__, url_prefix='/student')


# =========================
# 🔐 AUTH DECORATOR
# =========================
def student_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'student':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrap


# =========================
# 📊 DASHBOARD
# =========================
@student_bp.route('/dashboard')
@student_required
def dashboard():
    try:
        # Get student profile
        student = Student.query.filter_by(user_id=session['user_id']).first()

        if not student:
            return redirect(url_for('auth.login'))

        # Get marks
        marks_records = Mark.query.filter_by(student_id=student.id).all()

        # Calculate total & average
        total_marks = 0
        average_marks = 0.0

        if marks_records:
            total_marks = sum(m.marks for m in marks_records)
            average_marks = round(total_marks / len(marks_records), 2)

        return render_template(
            'student/dashboard.html',
            student=student,
            marks=marks_records,
            total_marks=total_marks,
            average_marks=average_marks
        )

    except Exception as e:
        print("Error loading student dashboard:", e)
        return render_template(
            'student/dashboard.html',
            student=None,
            marks=[],
            total_marks=0,
            average_marks=0
        )