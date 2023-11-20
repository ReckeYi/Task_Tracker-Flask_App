from flask_task import create_test_app
from flask_task.models import User

app = create_test_app()


class TestAddUser:
    def test_add_user(self, client, login):
        response = client.get('/add_user')
        assert response.status_code == 200
        assert b'<title>Flask Task - Add User</title>' in response.data

        response = client.post(
            '/add_user',
            data={
                'role_id': 1,
                'username': 'new_test_user',
                'email': 'new_test_user@test.com',
                'password': 'new_password',
                'confirm_password': 'new_password',
                'submit': True
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b'User has been created! You are now able to log in' in response.data
        assert b'<title>Flask Task - All Users</title>' in response.data

        with app.app_context():
            new_user = User.query.filter_by(username='new_test_user').first()
            assert new_user is not None
