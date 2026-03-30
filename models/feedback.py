from models import db

class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    role = db.Column(db.String(50))   # Student / Parent / Teacher

    message = db.Column(db.Text)

    status = db.Column(db.String(20), default="pending")  
    # pending / approved / rejected

    created_at = db.Column(db.DateTime, default=db.func.now())