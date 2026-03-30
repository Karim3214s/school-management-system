from models import db

class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    phone = db.Column(db.String(20))
    qualification = db.Column(db.String(100))
    experience = db.Column(db.Integer)
    address = db.Column(db.Text)
    photo = db.Column(db.String(200))


    # ✅ User relation (ONLY relation here)
    user_account = db.relationship(
        'User',
        backref='teacher_profile',
        uselist=False,
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Teacher ID:{self.id}>"