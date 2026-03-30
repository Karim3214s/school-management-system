from models import db

class Mark(db.Model):
    __tablename__ = 'marks'

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    teacher_assignment_id = db.Column(db.Integer, db.ForeignKey('teacher_assignments.id'), nullable=False)

    marks = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            'student_id',
            'subject_id',
            'teacher_assignment_id',
            name='unique_student_subject_assignment'
        ),
    )

    student = db.relationship('Student', backref='marks', lazy=True)
    subject = db.relationship('Subject', backref='marks', lazy=True)
    assignment = db.relationship('TeacherAssignment', backref='marks', lazy=True)

    def __repr__(self):
        return f"<Mark Student:{self.student_id} Subject:{self.subject_id} Marks:{self.marks}>"