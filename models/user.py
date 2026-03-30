from models import db

class User(db.Model):
    __tablename__ = 'users'

    # Columns
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(db.String(255), nullable=False)

    is_first_login = db.Column(db.Boolean, default=True)

    role = db.Column(
        db.String(20),
        nullable=False
    )  # admin / teacher / student

    def __repr__(self):
        return f"<User {self.email} - Role: {self.role}>"