from models import db

class TeacherAssignment(db.Model):
    __tablename__ = 'teacher_assignments'

    id = db.Column(db.Integer, primary_key=True)

    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)

    # ✅ ONLY DEFINE RELATIONSHIPS HERE (IMPORTANT 🔥)
    teacher = db.relationship(
    'Teacher',
    backref=db.backref('assignments', cascade="all, delete-orphan"),
    lazy=True
)
    class_ = db.relationship('ClassModel', backref='assignments', lazy=True)
    subject = db.relationship('Subject', backref='assignments', lazy=True)

    def __repr__(self):
        return f"<Assignment T:{self.teacher_id} C:{self.class_id} S:{self.subject_id}>"