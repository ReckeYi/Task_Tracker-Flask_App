import pytest
from datetime import datetime
from flask_task import create_test_app, db
from flask_task.models import Project, User, Task

app = create_test_app()


class TestModels:
    def test_count_users(self, users):
        with app.app_context():
            for user in users:
                db.session.add(user)
            db.session.commit()
            assert User.query.count() == 2

    def test_count_projects(self, projects):
        with app.app_context():
            for project in projects:
                db.session.add(project)
            db.session.commit()
            assert Project.query.count() == 2

    def test_count_tasks(self, tasks):
        with app.app_context():
            for task in tasks:
                db.session.add(task)
            db.session.commit()
            assert Task.query.count() == 2
