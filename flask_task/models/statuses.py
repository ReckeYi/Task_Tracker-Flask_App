from flask_task import db


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    status = db.Column(db.String(15), unique=True, nullable=False)

    def __init__(self, status: str):
        self.status = status

    def __repr__(self):
        return f"Status('{self.status}')"
