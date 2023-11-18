from flask_task import create_test_app
from flask_task.users.forms import LoginForm

class TestLoginForm:
    def test_valid_login(self, client):
        with client:
            with client.post('/login', data={
                'email': 'test@test.com',
                'password': 'password',
                'remember': False,
                'submit': True
            }) as response:
                form = LoginForm()
                assert form.validate() is True

    def test_invalid_email(self, client):
        with client:
            with client.post('/login', data={
                'email': 'test@example.test',
                'password': 'password',
                'remember': False,
                'submit': True
            }) as response:
                form = LoginForm()
                assert form.validate() is False

    def test_invalid_password(self, client):
        with client:
            with client.post('/login', data={
                'email': 'test@example.com',
                'password': '',
                'remember': False,
                'submit': True
            }) as response:
                form = LoginForm()
                assert form.validate() is False
