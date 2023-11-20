from flask_task import create_test_app
from flask_task.models import User

app = create_test_app()


class TestResetToken:
    def test_reset_request_token_user_is_authenticated(self, client, login):
        response = client.get('/reset_password', follow_redirects=True)
        assert response.status_code == 200
        assert b'<h1>Flask Task - Home Page</h1>' in response.data

    def test_reset_request_token_invalid_token(self, client):
        with app.app_context():
            reset_token = 'invalidresettoken'
        response = client.post('/reset_password/' + reset_token, follow_redirects=True)
        assert response.status_code == 200
        assert b'That is an invalid or expired token' in response.data
        assert b'<title>Flask Task - Reset Password</title>' in response.data

    def test_reset_request_token(self, client):
        with app.app_context():
            user = User.query.filter_by(username='test').first()
            reset_token = user.get_reset_token()
        response = client.post('/reset_password/' + reset_token,
                               data={
                                   'password': 'new_password',
                                   'confirm_password': 'new_password'
                               }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Your password has been updated! You are now able to log in' in response.data
        assert b'<title>Flask Task - Login</title>' in response.data
