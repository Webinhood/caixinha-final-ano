from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    credits_remaining = db.Column(db.Integer, default=3)
    is_winner = db.Column(db.Boolean, default=False)
    prize_code = db.Column(db.String(10), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    attempts = db.relationship('GameAttempt', backref='user', lazy=True)

class GameAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    attempt_number = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Boolean, default=False)  # True if won, False if lost
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
