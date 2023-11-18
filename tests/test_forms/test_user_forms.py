from flask_task import create_test_app
from flask_task.users.forms import LoginForm, RegistrationForm, UpdateAccountForm
from flask_bcrypt import Bcrypt

app = create_test_app()
bcrypt = Bcrypt()


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
                'email': 'test@test.test',
                'password': 'password',
                'remember': False,
                'submit': True
            }) as response:
                form = LoginForm()
                assert form.validate() is False

    def test_invalid_password(self, client):
        with client:
            with client.post('/login', data={
                'email': 'test@test.com',
                'password': '',
                'remember': False,
                'submit': True
            }) as response:
                form = LoginForm()
                assert form.validate() is False


class TestRegistrationForm:
    def test_valid_registration(self):
        with app.app_context():
            form = RegistrationForm(
                username='test_user2',
                email='test_user2@test.com',
                password='password',
                confirm_password='password',
                submit=True
            )
            assert form.validate() is True

    def test_duplicate_username_registration(self):
        with app.app_context():
            form = RegistrationForm(
                username='test',
                email='test_user@test.com',
                password='password',
                confirm_password='password',
                submit=True
            )
            assert form.validate() is False
            assert 'That username is taken. Please choose a different one.' in form.errors['username']

    #
    def test_duplicate_email_registration(self):
        with app.app_context():
            form = RegistrationForm(
                username='test_user',
                email='test@test.com',
                password='password',
                confirm_password='password',
                submit=True
            )
            assert form.validate() is False
            assert 'That email is taken. Please choose a different one.' in form.errors['email']
