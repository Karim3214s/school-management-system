from models import db

class Student(db.Model):
    __tablename__ = 'students'

    # Columns
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    class_id = db.Column(
        db.Integer,
        db.ForeignKey('classes.id'),
        nullable=False
    )

    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    parent_name = db.Column(db.String(100))
    parent_phone = db.Column(db.String(20))
    address = db.Column(db.Text)

    # Relationships

    # 🔥 Link to User (CRITICAL)
    user = db.relationship(
    'User',
    backref=db.backref('student', cascade="all, delete"),
    lazy=True
)

    # Marks handled from Mark model (backref='marks')
    # So no need to redefine differently

    def __repr__(self):
        return f"<Student ID:{self.id} Class:{self.class_id}>"