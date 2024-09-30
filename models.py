# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  user_id = db.Column(db.String(50), nullable=False)
  due_date = db.Column(db.DateTime, nullable=True)
  priority = db.Column(db.String(20), nullable=True)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

  def __repr__(self):
      return f"<Task {self.name}>"

class Timer(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.String(50), nullable=False)
  task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=True)
  start_time = db.Column(db.DateTime, default=datetime.utcnow)
  end_time = db.Column(db.DateTime, nullable=True)

  task = db.relationship('Task', backref=db.backref('timers', lazy=True))

  def __repr__(self):
      return f"<Timer User: {self.user_id}, Task: {self.task_id}>"

class UserPreference(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.String(50), unique=True, nullable=False)
  categories = db.Column(db.String(200), nullable=True)

  def __repr__(self):
      return f"<UserPreference {self.user_id}>"