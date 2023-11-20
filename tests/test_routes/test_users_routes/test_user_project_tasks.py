from flask_task import create_test_app
from flask_task.models import User, Project

app = create_test_app()


class TestUserProjectsTasks:
    def test_user_project_tasks(self, client, login):
        with app.app_context():
            user = User.query.filter_by(username='test').first()
            project = Project.query.filter_by(title='Test Project').first()
            response = client.get('/user/' + user.username + '/' + project.title)
            assert response.status_code == 200
            assert b'Tasks for' in response.data
            assert bytes(user.username, 'utf-8') in response.data
            assert bytes(project.title, 'utf-8') in response.data
            assert b'<title>Flask Task - User Project Tasks</title>' in response.data

    def test_user_project_tasks_invalid_username(self, client, login):
        with app.app_context():
            project = Project.query.filter_by(title='Test Project').first()
            response = client.get('/user/wrongusername/' + project.title)
            assert response.status_code == 404
            assert b'That page does not exist. Please try a different location' in response.data

    def test_user_project_tasks_invalid_project_title(self, client, login):
        with app.app_context():
            user = User.query.filter_by(username='test').first()
            response = client.get('/user/' + user.username + '/wrongprojecttitle')
            assert response.status_code == 404
            assert b'That page does not exist. Please try a different location' in response.data
