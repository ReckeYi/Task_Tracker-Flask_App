from sqlalchemy.orm import relationship
from flask_task import db
from datetime import datetime


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='task')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = relationship('Project', back_populates='task')
    deadline = db.Column(db.DateTime, nullable=False, default=None)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    status = relationship('Status', back_populates='task')

    def __init__(self, title: str, description: str, user_id: int, project_id: int, deadline: datetime, status_id: int):
        self.title = title
        self.description = description
        self.user_id = user_id
        self.project_id = project_id
        self.deadline = deadline
        self.status_id = status_id

    def __repr__(self):
        return f"Task('{self.title}', '{self.description}', '{self.user_id}', '{self.project_id}', '{self.deadline}'," \
               f"'{self.created_at}', '{self.status}')"
