
class TestResetRequest:
    def test_reset_request_user_is_authenticated(self, client, login):
        response = client.get('/reset_password', follow_redirects=True)
        assert response.status_code == 200
        assert b'<h1>Flask Task - Home Page</h1>' in response.data

    def test_reset_request(self, client):
        response = client.post('/reset_password',
                               data={
                                   'email': 'test@test.com',
                                   'submit': True
                               },
                               follow_redirects=True
                               )
        assert response.status_code == 200
        assert b'An email has been sent with instructions to reset your password.' in response.data
