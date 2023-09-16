from flask_task import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    role = db.Column(db.String(15), unique=True, nullable=False)

    def __init__(self, role: str):
        self.role = role

    def __repr__(self):
        return f"Role('{self.role}')"
