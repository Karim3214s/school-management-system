from flask import Blueprint, jsonify, render_template
from models.teacher import Teacher
from models.student import Student
from models.teacher import Teacher
from models.class_model import ClassModel
from models.subject import Subject
from models.contact_message import ContactMessage
from models import db
from flask import request, flash, redirect, url_for
from models.feedback import Feedback

common_bp = Blueprint('common', __name__, url_prefix='/')


# =========================
# 🏠 HOME
# =========================
@common_bp.route('/')
def home():

    return render_template(
        'common/index.html',

        total_students=Student.query.count(),
        total_teachers=Teacher.query.count(),
        total_classes=ClassModel.query.count(),
        total_subjects=Subject.query.count(),

        teachers=Teacher.query.all()  # already used below in your page
    )


# =========================
# ℹ️ ABOUT
# =========================
from models.feedback import Feedback

@common_bp.route('/about')
def about():

    feedbacks = Feedback.query.filter_by(status="approved").all()

    return render_template(
        'common/about.html',
        total_students=Student.query.count(),
        total_teachers=Teacher.query.count(),
        total_classes=ClassModel.query.count(),
        total_subjects=Subject.query.count(),
        feedbacks= Feedback.query.filter_by(status="approved")\
                          .order_by(Feedback.id.desc())\
                          .limit(5).all()   # 🔥 ADD THIS
    )


# =========================
# 👨‍🏫 FACULTY
# =========================
@common_bp.route('/faculty')
def faculty():
    try:
        # Fetch teachers with ordering
        teachers = Teacher.query.order_by(Teacher.id.desc()).all()

        return render_template('common/faculty.html', teachers=teachers)

    except Exception as e:
        print("Error loading faculty:", e)
        return render_template('common/faculty.html', teachers=[])


# =========================
# 📞 CONTACT
# =========================

@common_bp.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':
        msg = ContactMessage(
            name=request.form.get('name'),
            email=request.form.get('email'),
            subject=request.form.get('subject'),
            message=request.form.get('message')
        )

        db.session.add(msg)
        db.session.commit()

        flash("Message sent successfully!", "success")

        return redirect(url_for('common.contact'))

    return render_template('common/contact.html')

@common_bp.route('/feedback/add', methods=['POST'])
def add_feedback():

    name = request.form.get('name')
    role = request.form.get('role')
    message = request.form.get('message')
    rating = request.form.get('rating')

    fb = Feedback(
        name=name,
        role=role,
        message=message,
    )

    db.session.add(fb)
    db.session.commit()

    return jsonify({"status": "success"})