from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class TestRegistration:
    def test_register(self, client):
        hashed_password = bcrypt.generate_password_hash('test_password').decode('utf-8')
        response = client.post('/register', data={
            'username': 'test_user',
            'email': 'test_user@test.com',
            'password': hashed_password,
            'confirm_password': hashed_password,
            'submit': True
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Your account has been created! You are now able to log in' in response.data

    def test_register_duplicate_username(self, client):
        hashed_password = bcrypt.generate_password_hash('test_password').decode('utf-8')
        response = client.post('/register', data={
            'username': 'test',
            'email': 'test_user@test.com',
            'password': hashed_password,
            'confirm_password': hashed_password,
            'submit': True
        }, follow_redirects=True)
        assert b'That username is taken. Please choose a different one.' in response.data

    def test_register_duplicate_email(self, client):
        hashed_password = bcrypt.generate_password_hash('test_password').decode('utf-8')
        response = client.post('/register', data={
            'username': 'test_user',
            'email': 'test@test.com',
            'password': hashed_password,
            'confirm_password': hashed_password,
            'submit': True
        }, follow_redirects=True)
        assert b'That email is taken. Please choose a different one.' in response.data
