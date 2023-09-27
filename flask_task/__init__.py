from typing import Type

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_task.config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()


def create_app(config_class: Type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flask_task.users.routes import users
    from flask_task.projects.routes import projects
    from flask_task.tasks.routes import tasks
    from flask_task.main.routes import main
    from flask_task.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(projects)
    app.register_blueprint(tasks)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
