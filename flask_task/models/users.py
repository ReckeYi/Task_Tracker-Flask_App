from sqlalchemy.orm import relationship
from flask import current_app
from flask_task import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    roles = relationship('Role', backref='user')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def __init__(self, username: str, email: str, password: str, role_id: int = 1, image_file: str = None):
        self.username = username
        self.email = email
        self.password = password
        self.image_file = image_file
        self.role_id = role_id

    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.role_id}')"
