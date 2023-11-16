from flask_task import create_test_app, db
from flask_task.models import Project, User, Task

app = create_test_app()


class TestModels:
    def test_count_users(self, users):
        with app.app_context():
            for user in users:
                db.session.add(user)
            db.session.commit()

            user_q = User.query.filter_by(username='test').first()
            assert User.query.count() == 3
            assert User.query.first() is not None
            assert user_q.email == 'test@test.test'

            reset_token = user.get_reset_token()
            assert isinstance(reset_token, str) and len(reset_token) > 0

            verified_user = User.verify_reset_token(reset_token)
            assert verified_user is not None
            assert verified_user.id == user.id

    def test_count_projects(self, projects):
        with app.app_context():
            for project in projects:
                db.session.add(project)
            db.session.commit()

            project_q = Project.query.filter_by(title='Project TT1').first()
            assert Project.query.count() == 3
            assert project_q is not None
            assert project_q.title == 'Project TT1'
            assert project_q.user_id == 1
            assert project_q.user.username == 'test'
            assert project_q.user.email == 'test@test.test'

    def test_count_tasks(self, tasks):
        with app.app_context():
            for task in tasks:
                db.session.add(task)
            db.session.commit()

            task_q = Task.query.filter_by(title='Task TT1').first()
            assert Task.query.count() == 2
            assert task_q is not None
            assert task_q.title == 'Task TT1'
            assert task_q.description == 'Task Description'
            assert task_q.user_id == 1
            assert task_q.project_id == 1
            assert task_q.user.username == 'test'
            assert task_q.project.title == 'Test Project'
            assert task_q.status.status == 'In Progress'
