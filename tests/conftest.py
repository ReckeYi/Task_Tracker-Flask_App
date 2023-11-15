from datetime import datetime

import pytest
from flask_task import create_test_app, db
from flask_task.models import Role, Status, Task, Project, User

app = create_test_app()

'''DATABASE'''
@pytest.fixture(scope='session', autouse=True)
def setup_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

        roles = [
            Role(role='admin'),
            Role(role='manager'),
            Role(role='user')
        ]

        for role in roles:
            db.session.add(role)

        statuses = [
            Status(status="To Do"),
            Status(status="In Progress"),
            Status(status="Done"),
            Status(status="Closed")
        ]

        for status in statuses:
            db.session.add(status)

        db.session.commit()

'''MODELS'''

@pytest.fixture
def users():
    with app.app_context():
        users = [
            User(username='Devlog', email='devlog@delvog.com', password='password', role_id=1),
            User(username='Admin', email='admin@admin.com', password='password', role_id=2)
        ]
    return users


@pytest.fixture
def projects():
    with app.app_context():
        users = User.query.all()
        for user in users:
            user_id = user.id

        projects = [
            Project(title='Project TT1', description='Description of a project', user_id=user_id),
            Project(title='Project TT2', description='Description of a project', user_id=user_id)
        ]

    return projects


@pytest.fixture
def tasks():
    with app.app_context():
        users = User.query.all()
        for user in users:
            user_id = user.id

        projects = Project.query.all()
        for project in projects:
            project_id = project.id

        tasks = [
            Task(title='Task TT1', description='Task Description', user_id=user_id, project_id=project_id,
                 deadline=datetime.today(), status_id=2),
            Task(title='Task TT2', description='Task Description', user_id=user_id, project_id=project_id,
                 deadline=datetime.today(), status_id=2)
        ]

    return tasks