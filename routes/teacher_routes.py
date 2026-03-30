from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from functools import wraps
from models import db
from models.teacher import Teacher
from models.student import Student
from models.assignment import TeacherAssignment
from models.marks import Mark

teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')


# =========================
# 🔐 AUTH DECORATOR
# =========================
def teacher_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'teacher':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrap


# =========================
# 👨‍🏫 GET LOGGED-IN TEACHER (NEW 🔥)
# =========================
def get_current_teacher():
    return Teacher.query.filter_by(user_id=session['user_id']).first()


# =========================
# 📊 DASHBOARD
# =========================
@teacher_bp.route('/dashboard')
@teacher_required
def dashboard():
    teacher = get_current_teacher()

    if not teacher:
        return redirect(url_for('auth.login'))

    assignments = TeacherAssignment.query.filter_by(teacher_id=teacher.id).all()

    class_ids = {a.class_id for a in assignments}
    subject_ids = {a.subject_id for a in assignments}

    total_students = Student.query.filter(
        Student.class_id.in_(class_ids)
    ).count() if class_ids else 0

    stats = {
        'assigned_classes': len(class_ids),
        'assigned_subjects': len(subject_ids),
        'total_students': total_students
    }

    return render_template(
        'teacher/dashboard.html',
        teacher=teacher,
        stats=stats,
        assignments=assignments
    )


# =========================
# 📋 ASSIGNMENTS PAGE
# =========================
@teacher_bp.route('/assignments')
@teacher_required
def assignments():
    teacher = get_current_teacher()

    if not teacher:
        return redirect(url_for('auth.login'))

    assignments = TeacherAssignment.query.filter_by(
        teacher_id=teacher.id
    ).all()

    return render_template(
        'teacher/assignments.html',
        teacher=teacher,
        assignments=assignments
    )


# =========================
# 👨‍🎓 STUDENTS (BY ASSIGNMENT)
# =========================
@teacher_bp.route('/students/<int:assignment_id>')
@teacher_required
def students(assignment_id):

    teacher = get_current_teacher()
    if not teacher:
        return redirect(url_for('auth.login'))

    assignment = TeacherAssignment.query.get(assignment_id)

    if not assignment or assignment.teacher_id != teacher.id:
        return redirect(url_for('teacher.dashboard'))

    students = Student.query.filter_by(class_id=assignment.class_id).all()

    # 🔥 optimized marks fetch
    marks = Mark.query.filter_by(
        subject_id=assignment.subject_id,
        teacher_assignment_id=assignment.id
    ).all()

    marks_dict = {m.student_id: m.marks for m in marks}

    student_data = []

    for student in students:
        student_data.append({
            "id": student.id,
            "name": student.user.name,
            "marks": marks_dict.get(student.id)
        })

    return render_template(
        'teacher/students.html',
        teacher=teacher,
        students=student_data,
        selected_class=assignment.class_,
        selected_subject=assignment.subject,
        assignment_id=assignment.id
    )


# =========================
# ✏️ ADD / UPDATE MARKS
# =========================
@teacher_bp.route('/add-marks', methods=['POST'])
@teacher_required
def add_marks():
    try:
        data = request.get_json()

        student_id = data.get('student_id')
        assignment_id = data.get('assignment_id')
        marks_value = data.get('marks')

        if not student_id or not assignment_id or marks_value is None:
            return jsonify({"status": "error", "message": "Missing data"}), 400

        # 🔥 FIX: convert to int
        marks_value = int(marks_value)

        if marks_value < 0 or marks_value > 100:
            return jsonify({"status": "error", "message": "Invalid marks"}), 400

        teacher = get_current_teacher()
        if not teacher:
            return jsonify({"status": "error", "message": "Unauthorized"}), 403

        assignment = db.session.get(TeacherAssignment, assignment_id)

        if not assignment or assignment.teacher_id != teacher.id:
            return jsonify({"status": "error", "message": "Unauthorized"}), 403

        # 🔥 OPTIONAL SAFETY
        student = db.session.get(Student, student_id)
        if not student:
            return jsonify({"status": "error", "message": "Student not found"}), 404

        existing = Mark.query.filter_by(
            student_id=student_id,
            subject_id=assignment.subject_id,
            teacher_assignment_id=assignment_id
        ).first()

        if existing:
            existing.marks = marks_value
        else:
            db.session.add(Mark(
                student_id=student_id,
                subject_id=assignment.subject_id,
                teacher_assignment_id=assignment_id,
                marks=marks_value
            ))

        db.session.commit()

        return jsonify({"status": "success"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    
@teacher_bp.route('/my-students')
@teacher_required
def my_students():

    teacher = get_current_teacher()

    assignments = TeacherAssignment.query.filter_by(
        teacher_id=teacher.id
    ).all()

    data = []
    class_set = set()
    subject_set = set()

    for a in assignments:

        class_set.add(a.class_.class_name)
        subject_set.add(a.subject.subject_name)

        students = Student.query.filter_by(class_id=a.class_id).all()

        for s in students:

            mark = Mark.query.filter_by(
                student_id=s.id,
                subject_id=a.subject_id,
                teacher_assignment_id=a.id
            ).first()

            data.append({
                "student_id": s.id,
                "name": s.user.name,
                "class": a.class_.class_name,
                "subject": a.subject.subject_name,
                "marks": mark.marks if mark else None,
                "assignment_id": a.id
            })

    return render_template(
        "teacher/my_students.html",
        students=data,
        classes=list(class_set),
        subjects=list(subject_set),
        teacher=teacher
    )

@teacher_bp.route('/my-classes')
@teacher_required
def my_classes():

    teacher = get_current_teacher()

    if not teacher:
        return redirect(url_for('auth.login'))

    assignments = TeacherAssignment.query.filter_by(
        teacher_id=teacher.id   # ✅ CORRECT
    ).all()

    return render_template(
        'teacher/my_classes.html',
        assignments=assignments,
        teacher=teacher
    )

@teacher_bp.route('/profile')
@teacher_required
def profile():

    teacher = get_current_teacher()

    if not teacher:
        return redirect(url_for('auth.login'))

    return render_template(
        'teacher/profile.html',
        teacher=teacher
    )