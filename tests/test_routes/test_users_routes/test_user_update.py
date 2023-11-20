from flask_task import create_test_app
from flask_task.models import User

app = create_test_app()


class TestUserUpdate:
    def test_update_account_valid(self, client, login):
        with app.app_context():
            user = User.query.filter_by(username='test').first()
            # username = user.username
            response = client.post('/user/update/' + user.username, data={
                'role_id': 1,
                'username': 'test-test',
                'email': 'test@test.com',
                'picture': None,
                'submit': True
            }
                                   )
            updated_user = User.query.filter_by(username='test-test').first()
            assert updated_user is not None

    def test_update_account_duplicate_username(self, client, login):
        with app.app_context():
            user = User.query.filter_by(username='test-test').first()
            response = client.post('/user/update/' + user.username, data={
                'role_id': 1,
                'username': 'test2',
                'email': 'test@test.com',
                'picture': None,
                'submit': True
            }
                                   )
            assert b'That username is taken. Please choose a different one.' in response.data

    def test_update_account_duplicate_email(self, client, login):
        with app.app_context():
            user = User.query.filter_by(username='test-test').first()
            response = client.post('/user/update/' + user.username, data={
                'role_id': 1,
                'username': 'test-test',
                'email': 'test2@test.com',
                'picture': None,
                'submit': True
            }
                                   )
            assert b'That email is taken. Please choose a different one.' in response.data
