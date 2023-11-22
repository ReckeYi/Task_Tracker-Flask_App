from datetime import datetime

import pytest
from flask_bcrypt import Bcrypt

from flask_task import create_test_app, db
from flask_task.models import Role, Status, Task, Project, User

app = create_test_app()
bcrypt = Bcrypt()


@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()

    return client


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

        hashed_test_password = bcrypt.generate_password_hash('test').decode('utf-8')

        users = [
            User(username='test', email='test@test.com', password=hashed_test_password, role_id=1),
            User(username='test2', email='test2@test.com', password=hashed_test_password, role_id=1),
            User(username='test3', email='test3@test.com', password=hashed_test_password, role_id=1),
            User(username='test4', email='test4@test.com', password=hashed_test_password, role_id=1)
        ]

        for user in users:
            db.session.add(user)

        project = Project(title='Test Project', description='Description of a project', user_id=1)
        db.session.add(project)

        db.session.commit()


'''MODELS'''


@pytest.fixture
def users():
    with app.app_context():
        hashed_password = bcrypt.generate_password_hash('test').decode('utf-8')
        users = [
            User(username='Devlog', email='devlog@delvog.com', password=hashed_password, role_id=1),
            User(username='Admin', email='admin@admin.com', password=hashed_password, role_id=2)
        ]
    return users


@pytest.fixture
def projects():
    with app.app_context():
        projects = [
            Project(title='Project TT1', description='Description of a project', user_id=1),
            Project(title='Project TT2', description='Description of a project', user_id=1)
        ]

    return projects


@pytest.fixture
def tasks():
    with app.app_context():
        tasks = [
            Task(title='Task TT1', description='Task Description', user_id=1, project_id=1,
                 deadline=datetime.today(), status_id=2),
            Task(title='Task TT2', description='Task Description', user_id=1, project_id=1,
                 deadline=datetime.today(), status_id=2)
        ]

    return tasks


'''LOGIN'''


@pytest.fixture
def login(client):
    response = client.post('/login', data={
        'email': 'test@test.com',
        'password': 'test',
        'remember': True,
        'submit': True,
    }, follow_redirects=True)

    return login
