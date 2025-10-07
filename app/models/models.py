from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    team = db.Column(db.String(50))
    answers = db.relationship('Answer', backref='student', lazy=True)


class Statement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    choice1_text = db.Column(db.String(255), nullable=False)
    choice1_letter = db.Column(db.String(1), nullable=False)
    choice2_text = db.Column(db.String(255), nullable=False)
    choice2_letter = db.Column(db.String(1), nullable=False)
    answers = db.relationship('Answer', backref='statement', lazy=True)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    statement_id = db.Column(db.Integer, db.ForeignKey('statement.id'), nullable=False)
    choice_number = db.Column(db.Integer, nullable=False)  # 1 of 2
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):  # Voor docenten
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, plaintext: str):
        # PBKDF2-SHA256 hash met unieke salt
        self.password_hash = generate_password_hash(
            plaintext,
            method="pbkdf2:sha256",   # expliciet maken
            salt_length=16            # unieke salt per gebruiker
        )

    def check_password(self, plaintext: str) -> bool:
        return check_password_hash(self.password_hash, plaintext)
