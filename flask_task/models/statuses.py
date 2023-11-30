from sqlalchemy.orm import relationship

from flask_task import db


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.String(15), unique=True, nullable=False)
    task = relationship('Task', back_populates='status')

    def __init__(self, status: str):
        self.status = status

    def __repr__(self):
        return f"Status('{self.status}')"
