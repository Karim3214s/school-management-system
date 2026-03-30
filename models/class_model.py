from models import db

class ClassModel(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False, unique=True)

    # One class → many students
    students = db.relationship(
    'Student',
    backref='class_',
    cascade="all, delete",
    lazy=True
)

    def __repr__(self):
        return f"<Class {self.class_name}>"