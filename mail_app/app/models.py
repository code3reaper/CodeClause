from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    smtp_settings = db.relationship('SMTPSettings', backref='owner', lazy=True)

class SMTPSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    smtp_server = db.Column(db.String(120), nullable=False)
    smtp_port = db.Column(db.Integer, nullable=False)
    smtp_username = db.Column(db.String(120), nullable=False)
    smtp_password = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class SentEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    recipient = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
