from flask_task import create_test_app
from flask_task.models import User

app = create_test_app()


class TestUserTasks:
    def test_user_project_tasks(self, client, login):
        with app.app_context():
            user = User.query.filter_by(email='test@test.com').first()
            response = client.get('/user/tasks/' + user.username)
            user_2 = User.query.filter_by(email='test@test.com').first()
            response_2 = client.get('/user/tasks/' + user.username)
            assert response.status_code == 200
            assert b'Tasks for' in response.data
            assert bytes(user.username, 'utf-8') in response.data
            assert b'<title>Flask Task - User Tasks</title>' in response.data
            assert response_2.status_code == 200
            assert b'Tasks for' in response_2.data
            assert bytes(user_2.username, 'utf-8') in response_2.data
            assert b'<title>Flask Task - User Tasks</title>' in response_2.data

    def test_user_project_tasks_invalid_username(self, client, login):
        with app.app_context():
            response = client.get('/user/tasks/wrongusername/')
            assert response.status_code == 404
            assert b'That page does not exist. Please try a different location' in response.data
