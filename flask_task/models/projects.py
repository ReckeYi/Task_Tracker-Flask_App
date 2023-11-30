from sqlalchemy.orm import relationship
from flask_task import db
from datetime import datetime


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='project')
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    engage = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    task = relationship('Task', back_populates='project', cascade='all, delete-orphan')

    def __init__(self, title: str, description: str, user_id: int):
        self.title = title
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return f"Project('{self.title}', '{self.description}', '{self.user_id}', '{self.created}', '{self.engage}')"
