class TestUsersList:
    def test_users_list_user_is_authenticated(self, client, login):
        response = client.get('/users')
        assert response.status_code == 200
        assert b'<title>Flask Task - All Users</title>' in response.data

    def test_users_list_user_is_not_authenticated(self, client):
        response = client.get('/users', follow_redirects=True)
        assert response.status_code == 200
        assert b'<title>Flask Task - Login</title>' in response.data
        assert b'Please log in to access this page.' in response.data
