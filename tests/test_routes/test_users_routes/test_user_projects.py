from flask_task import create_test_app
from flask_task.models import User

app = create_test_app()


class TestUserProjects:
    def test_user_projects_valid_username(self, client, login):
        with app.app_context():
            user = User.query.filter_by(username='test').first()
            response = client.get('/user/' + user.username)
            assert response.status_code == 200
            assert b'Projects by' in response.data
            assert bytes(user.username, 'utf-8') in response.data
            assert b'<title>Flask Task - User Projects</title>' in response.data

    def test_user_projects_invalid_username(self, client, login):
        with app.app_context():
            response = client.get('/user/wrongusername')
            assert response.status_code == 404
            assert b'That page does not exist. Please try a different location' in response.data
