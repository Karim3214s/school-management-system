from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, current_app
from werkzeug.security import generate_password_hash
from flask_mail import Message
from extensions import mail
from functools import wraps
import random
import string

from models import db
from models.user import User
from models.teacher import Teacher
from models.student import Student
from models.class_model import ClassModel
from models.subject import Subject
from models.assignment import TeacherAssignment
from models.contact_message import ContactMessage
from models.feedback import Feedback
from werkzeug.utils import secure_filename
from flask import current_app


from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = "static/uploads"

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# =========================
# 🔐 AUTH
# =========================
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrap


# =========================
# 🔑 PASSWORD
# =========================
def generate_password(length=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


# =========================
# 📧 EMAIL
# =========================
def send_credentials_email(email, name, password):
    try:
        msg = Message(
            subject="Your School Portal Credentials",
            recipients=[email]
        )

        msg.body = f"""
Hello {name},

Your account has been created.

Email: {email}
Password: {password}

Please login and change your password.

Regards,
School Admin
"""
        mail.send(msg)

        print("✅ Mail sent successfully")
        current_app.extensions['mail'].send(msg)

    except Exception as e:
        print("Email error:", e)


# =========================
# 📊 DASHBOARD
# =========================
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    return render_template("admin/dashboard.html",
        stats={
            "total_students": Student.query.count(),
            "total_teachers": Teacher.query.count(),
            "total_classes": ClassModel.query.count(),
            "total_subjects": Subject.query.count()
        }
    )


# =========================
# 📄 PAGES
# =========================
@admin_bp.route('/manage-teachers')
def manage_teachers():

    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)

    query = Teacher.query.join(User)

    if search:
        query = query.filter(User.name.ilike(f"%{search}%"))

    teachers = query.paginate(page=page, per_page=2)

    return render_template(
        'admin/manage_teachers.html',
        teachers=teachers,
        search=search
    )

@admin_bp.route('/manage-students')
def manage_students():

    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)

    query = Student.query.join(User)

    if search:
        query = query.filter(User.name.ilike(f"%{search}%"))

    students = query.paginate(page=page, per_page=5)

    return render_template(
        'admin/manage_students.html',
        students=students,
        classes=ClassModel.query.all(),  # 🔥 REQUIRED
        search=search
    )

@admin_bp.route('/manage-classes')
@admin_required
def manage_classes():

    page = request.args.get('page', 1, type=int)

    classes = ClassModel.query.paginate(
        page=page,
        per_page=2,
        error_out=False
    )

    return render_template(
        "admin/manage_classes.html",
        classes=classes
    )


@admin_bp.route('/manage-subjects')
@admin_required
def manage_subjects():

    page = request.args.get('page', 1, type=int)

    subjects = Subject.query.paginate(
        page=page,
        per_page=5,
        error_out=False
    )

    return render_template(
        "admin/manage_subjects.html",
        subjects=subjects
    )



@admin_bp.route('/assign-teachers')
@admin_required
def assign_teachers():

    page = request.args.get('page', 1, type=int)

    assignments = TeacherAssignment.query.paginate(
        page=page,
        per_page=2,
        error_out=False
    )

    teachers = Teacher.query.all()
    classes = ClassModel.query.all()
    subjects = Subject.query.all()

    return render_template(
        "admin/assign_teachers.html",
        assignments=assignments,
        teachers=teachers,
        classes=classes,
        subjects=subjects
    )


@admin_bp.route('/search-students')
def search_students():

    search = request.args.get('search', '', type=str)

    query = Student.query.join(User)

    if search:
        query = query.filter(User.name.ilike(f"%{search}%"))

    students = query.all()

    result = []

    for s in students:
        result.append({
            "id": s.id,
            "name": s.user.name,
            "email": s.user.email,
            "class": s.class_.class_name if s.class_ else "-",
            "age": s.age,
            "gender": s.gender
        })

    return jsonify(result)

@admin_bp.route('/search-teachers')
def search_teachers():

    search = request.args.get('search', '', type=str)

    query = Teacher.query.join(User)

    if search:
        query = query.filter(User.name.ilike(f"%{search}%"))

    teachers = query.all()

    result = []

    for t in teachers:
        result.append({
            "id": t.id,
            "name": t.user_account.name,
            "email": t.user_account.email,
            "qualification": t.qualification,
            "experience": t.experience,
            "photo": t.photo
        })

    return jsonify(result)

# =========================
# ➕ ADD CLASS
# =========================
@admin_bp.route('/add-class', methods=['POST'])
@admin_required
def add_class():
    try:
        data = request.get_json()
        name = data.get('class_name')
        name = name.strip().upper()

        if not name:
            return jsonify({"status": "error", "message": "Class name required"}), 400

        existing = ClassModel.query.filter_by(class_name=name).first()
        if existing:
            return jsonify({
                "status": "exists",
                "message": "Class already exists"
            })

        new_class = ClassModel(class_name=name)
        db.session.add(new_class)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Class added successfully",
            "class": {
                "id": new_class.id,
                "class_name": new_class.class_name
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# =========================
# ➕ ADD SUBJECT
# =========================
@admin_bp.route('/add-subject', methods=['POST'])
@admin_required
def add_subject():
    try:
        data = request.get_json()
        name = data.get('subject_name')

        if not name:
            return jsonify({"status": "error", "message": "Subject name required"}), 400

        existing = Subject.query.filter_by(subject_name=name).first()
        if existing:
            return jsonify({"status": "error", "message": "Subject already exists"})

        new_subject = Subject(subject_name=name)
        db.session.add(new_subject)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Subject added successfully"
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# =========================
# ➕ ADD TEACHER
# =========================
@admin_bp.route('/add-teacher', methods=['POST'])
@admin_required
def add_teacher():
    try:
        name = request.form.get('name')
        email = request.form.get('email')

        password = generate_password()

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role='teacher'
        )

        db.session.add(user)
        db.session.flush()

        # 🔥 HANDLE IMAGE
        file = request.files.get("photo")
        filename = None

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        teacher = Teacher(
            user_id=user.id,
            phone=request.form.get('phone'),
            qualification=request.form.get('qualification'),
            experience=request.form.get('experience'),
            address=request.form.get('address'),
            photo=filename   # 🔥 SAVE
        )

        db.session.add(teacher)
        db.session.commit()

        send_credentials_email(email, name, password)

        return jsonify({"status": "success"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)})

# =========================
# ➕ ADD STUDENT
# =========================
@admin_bp.route('/add-student', methods=['POST'])
@admin_required
def add_student():
    try:
        data = request.get_json()

        if not data.get('name') or not data.get('email'):
            return jsonify({"status": "error", "message": "Name and Email required"}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({"status": "error", "message": "Email already exists"}), 400

        password = generate_password()

        user = User(
            name=data['name'],
            email=data['email'],
            password=generate_password_hash(password),
            role='student'
        )

        db.session.add(user)
        db.session.flush()

        student = Student(
            user_id=user.id,
            class_id=data.get('class_id'),
            age=data.get('age'),
            gender=data.get('gender'),
            parent_name=data.get('parent_name'),
            parent_phone=data.get('parent_phone'),
            address=data.get('address')
        )

        db.session.add(student)
        db.session.commit()

        send_credentials_email(data['email'], data['name'], password)

        return jsonify({
            "status": "success",
            "message": "Student added successfully"
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500




# =========================
# ➕ ASSIGN TEACHER
# =========================
@admin_bp.route('/assign-teacher', methods=['POST'])
@admin_required
def assign_teacher():
    try:
        data = request.get_json()

        teacher_id = data.get('teacher_id')
        class_id = data.get('class_id')
        subject_id = data.get('subject_id')

        # 🔥 CHECK DUPLICATE
        existing = TeacherAssignment.query.filter_by(
            class_id=class_id,
            subject_id=subject_id
        ).first()

        if existing:
            return jsonify({
                "status": "exists",
                "message": "This subject is already assigned to another teacher"
            })

        assignment = TeacherAssignment(
            teacher_id=teacher_id,
            class_id=class_id,
            subject_id=subject_id
        )

        db.session.add(assignment)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Assigned successfully"
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    
# =========================
# 🗑 DELETE
# =========================
@admin_bp.route('/delete-class/<int:id>', methods=['DELETE'])
@admin_required
def delete_class(id):
    db.session.delete(ClassModel.query.get(id))
    db.session.commit()
    return jsonify({"status": "success", "message": "Class deleted"})


@admin_bp.route('/delete-subject/<int:id>', methods=['DELETE'])
@admin_required
def delete_subject(id):
    db.session.delete(Subject.query.get(id))
    db.session.commit()
    return jsonify({"status": "success", "message": "Subject deleted"})


@admin_bp.route('/delete-teacher/<int:id>', methods=['DELETE'])
@admin_required
def delete_teacher(id):
    t = Teacher.query.get(id)
    u = User.query.get(t.user_id)
    db.session.delete(t)
    db.session.delete(u)
    db.session.commit()
    return jsonify({"status": "success", "message": "Teacher deleted"})


@admin_bp.route('/delete-student/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        student = Student.query.get(id)

        if not student:
            return jsonify({"status": "error", "message": "Student not found"}), 404

        user = User.query.get(student.user_id)

        db.session.delete(student)
        db.session.delete(user)   # 🔥 IMPORTANT FIX

        db.session.commit()

        return jsonify({"status": "success"})

    except Exception as e:
        print("Delete error:", e)
        return jsonify({"status": "error"}), 500

@admin_bp.route('/get-classes')
def get_classes():
    classes = ClassModel.query.all()
    return jsonify([
        {"id": c.id, "class_name": c.class_name}
        for c in classes
    ])


# =========================
# 👁 GET STUDENT (REQUIRED)
# =========================
@admin_bp.route('/get-student/<int:id>')
@admin_required
def get_student(id):

    student = Student.query.get(id)

    if not student:
        return jsonify({"status": "error", "message": "Student not found"}), 404

    cls = ClassModel.query.get(student.class_id)

    return jsonify({
        "name": student.user.name if student.user else "",
        "email": student.user.email if student.user else "",
        "class": cls.class_name if cls else "",
        "class_id": student.class_id,
        "age": student.age,
        "gender": student.gender,
        "parent_name": student.parent_name,
        "parent_phone": student.parent_phone,
        "address": student.address
    })



# =========================
# ✏️ UPDATE STUDENT
# =========================
@admin_bp.route('/update-student/<int:id>', methods=['PUT'])
@admin_required
def update_student(id):
    try:
        data = request.get_json()

        student = Student.query.get(id)
        if not student:
            return jsonify({"status": "error", "message": "Student not found"}), 404

        user = User.query.get(student.user_id)

        # update user
        user.name = data.get('name')
        user.email = data.get('email')

        # update student
        student.class_id = data.get('class_id')
        student.age = data.get('age')
        student.gender = data.get('gender')
        student.parent_name = data.get('parent_name')
        student.parent_phone = data.get('parent_phone')
        student.address = data.get('address')

        db.session.commit()

        return jsonify({"status": "success", "message": "Student updated successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    

@admin_bp.route('/get-class/<int:id>')
@admin_required
def get_class(id):
    c = ClassModel.query.get(id)

    if not c:
        return jsonify({"status": "error", "message": "Class not found"}), 404

    return jsonify({
        "id": c.id,
        "class_name": c.class_name
    })


@admin_bp.route('/update-class/<int:id>', methods=['PUT'])
@admin_required
def update_class(id):
    try:
        data = request.get_json()

        c = ClassModel.query.get(id)

        if not c:
            return jsonify({"status": "error", "message": "Class not found"}), 404

        c.class_name = data.get("class_name")

        db.session.commit()

        return jsonify({"status": "success", "message": "Class updated successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    

@admin_bp.route('/get-subject/<int:id>')
@admin_required
def get_subject(id):
    s = Subject.query.get(id)

    if not s:
        return jsonify({"status": "error", "message": "Subject not found"}), 404

    return jsonify({
        "id": s.id,
        "subject_name": s.subject_name
    })

@admin_bp.route('/update-subject/<int:id>', methods=['PUT'])
@admin_required
def update_subject(id):
    try:
        data = request.get_json()

        s = Subject.query.get(id)

        if not s:
            return jsonify({"status": "error", "message": "Subject not found"}), 404

        s.subject_name = data.get("subject_name")

        db.session.commit()

        return jsonify({"status": "success", "message": "Subject updated successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    

# =========================
# 👁 GET TEACHER (FIX VIEW/EDIT)
# =========================
@admin_bp.route('/get-teacher/<int:id>')
@admin_required
def get_teacher(id):

    teacher = Teacher.query.get(id)

    if not teacher:
        return jsonify({"status": "error", "message": "Teacher not found"}), 404

    user = User.query.get(teacher.user_id)

    return jsonify({
        "name": user.name if user else "",
        "email": user.email if user else "",
        "phone": teacher.phone,
        "qualification": teacher.qualification,
        "experience": teacher.experience,
        "address": teacher.address
    })


# =========================
# ✏️ UPDATE TEACHER
# =========================
@admin_bp.route('/update-teacher/<int:id>', methods=['PUT'])
@admin_required
def update_teacher(id):
    try:
        data = request.get_json()

        teacher = Teacher.query.get(id)
        if not teacher:
            return jsonify({"status": "error", "message": "Teacher not found"}), 404

        user = User.query.get(teacher.user_id)

        # update user
        user.name = data.get('name')
        user.email = data.get('email')

        # update teacher
        teacher.phone = data.get('phone')
        teacher.qualification = data.get('qualification')
        teacher.experience = data.get('experience')
        teacher.address = data.get('address')

        db.session.commit()

        return jsonify({"status": "success", "message": "Teacher updated successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    

@admin_bp.route('/delete-assignment/<int:id>', methods=['DELETE'])
@admin_required
def delete_assignment(id):
    db.session.delete(TeacherAssignment.query.get(id))
    db.session.commit()
    return jsonify({"status": "success", "message": "Assignment deleted"})

@admin_bp.route('/get-assignment/<int:id>')
@admin_required
def get_assignment(id):

    a = TeacherAssignment.query.get(id)

    if not a:
        return jsonify({"status": "error"}), 404

    return jsonify({
        "id": a.id,
        "teacher_id": a.teacher_id,
        "class_id": a.class_id,
        "subject_id": a.subject_id
    })



@admin_bp.route('/update-assignment/<int:id>', methods=['PUT'])
@admin_required
def update_assignment(id):
    try:
        data = request.get_json()

        a = TeacherAssignment.query.get(id)
        class_id = data.get('class_id')
        subject_id = data.get('subject_id')

        if not a:
            return jsonify({"status": "error"}), 404

        # 🔥 duplicate check
        existing = TeacherAssignment.query.filter(
            TeacherAssignment.class_id == class_id,
            TeacherAssignment.subject_id == subject_id,
            TeacherAssignment.id != id   # 🔥 exclude current row
        ).first()

        if existing:
            return jsonify({
                "status": "exists",
                "message": "This subject is already assigned to another teacher"
            })

        a.teacher_id = data['teacher_id']
        a.class_id = data['class_id']
        a.subject_id = data['subject_id']

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Updated successfully"
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    

@admin_bp.route('/messages')
def messages():

    page = request.args.get('page', 1, type=int)
    per_page = 5  # 🔥 number of rows per page

    pagination = ContactMessage.query.order_by(
        ContactMessage.id.desc()
    ).paginate(page=page, per_page=per_page)

    return render_template(
        'admin/messages.html',
        messages=pagination.items,
        pagination=pagination
    )


@admin_bp.route('/reply/<int:id>', methods=['POST'])
def reply_message(id):

    try:
        msg = ContactMessage.query.get(id)

        data = request.get_json()
        reply_text = data.get("reply")

        # Save reply
        msg.reply = reply_text
        db.session.commit()

        # 🔥 OPTIONAL MAIL (SAFE TRY)
        try:
            from flask_mail import Message
            from app import mail

            email_msg = Message(
                subject="Reply from School",
                recipients=[msg.email],
                body=reply_text
            )
            mail.send(email_msg)

        except Exception as e:
            print("Mail error:", e)  # don't break system

        return jsonify({
            "status": "success",
            "reply": reply_text
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({
            "status": "error",
            "message": "Server error"
        }), 500
    
@admin_bp.route('/feedbacks')
def feedbacks():

    feedbacks = Feedback.query.order_by(Feedback.id.desc()).all()

    return render_template('admin/feedbacks.html', feedbacks=feedbacks)

@admin_bp.route('/feedback/approve/<int:id>', methods=['POST'])
def approve_feedback(id):
    fb = Feedback.query.get(id)
    fb.status = "approved"
    db.session.commit()
    return jsonify({"status": "success"})


@admin_bp.route('/feedback/reject/<int:id>', methods=['POST'])
def reject_feedback(id):
    fb = Feedback.query.get(id)
    fb.status = "rejected"
    db.session.commit()
    return jsonify({"status": "success"})