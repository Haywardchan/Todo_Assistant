from datetime import datetime, date
from .base import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=True)
    end_time = db.Column(db.Time, nullable=True)
    group = db.Column(db.String(50), nullable=True)
    parent_group = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def remaining_days(self):
        if not self.due_date:
            return None
        today = date.today()
        delta = self.due_date - today
        return delta.days

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'remaining_days': self.remaining_days(),
            'group': self.group,
            'parent_group': self.parent_group
        }
