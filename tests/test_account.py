from flask_task import create_test_app
from flask_task.models import User

app = create_test_app()


class TestUpdateAccountForm:

    def test_valid_update_account(self, client, login):
        response = client.post('/account', data={
            'role_id': 1,
            'username': 'test-test',
            'email': 'test@test.com',
            'picture': None,
            'submit': True
        }
                               )

        with app.app_context():
            updated_user = User.query.filter_by(username='test-test').first()
            assert updated_user is not None

    def test_duplicate_username_update_account(self, client, login):
        response = client.post(
            '/account', data={
                'role_id': 1,
                'username': 'test2',
                'email': 'test@test.com',
                'picture': None,
                'submit': True
            }, follow_redirects=True
        )
        assert b'That username is taken. Please choose a different one.' in response.data

    def test_duplicate_email_update_account(self, client, login):
        response = client.post(
            '/account', data={
                'role_id': 1,
                'username': 'test',
                'email': 'test2@test.com',
                'picture': None,
                'submit': True
            }, follow_redirects=True
        )
        assert b'That email is taken. Please choose a different one.' in response.data
