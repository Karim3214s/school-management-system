from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models here so db.create_all() can see them
from models.user import User
from models.teacher import Teacher
from models.student import Student
from models.class_model import ClassModel
from models.subject import Subject
from models.assignment import TeacherAssignment
from models.marks import Mark