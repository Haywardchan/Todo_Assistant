from flask_login import UserMixin
from .base import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    todos = db.relationship('Todo', backref='user', lazy=True)
    groups = db.relationship('Group', backref='user', lazy=True)
