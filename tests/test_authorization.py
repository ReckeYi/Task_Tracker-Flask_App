import re
from flask_bcrypt import Bcrypt
from flask_task import create_test_app

app = create_test_app()
bcrypt = Bcrypt()

class TestLogin:
    def test_login(self, client):
        response = client.get('/login')
        assert response.status_code == 200

        # Extract the CSRF token from the HTML content
        csrf_token = None
        content = response.data.decode('utf-8')
        token_start = content.find('name="csrf_token"') + len('name="csrf_token"') + 1
        token_end = content.find('>', token_start)
        csrf_token = content[token_start:token_end - 1]
        csrf_token_element = re.search(r'<input.*?id="csrf_token".*?>', content)
        if csrf_token_element:
            csrf_token_value = re.search(r'value="(.*?)"', csrf_token_element.group()).group(1)

        response = client.post('/login', data={
            'email': 'test@test.com',
            'password': 'test',
            'remember': True,
            'submit': True,
            'csrf_token': csrf_token_value
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'<h1>Flask Task - Home Page</h1>' in response.data

    def test_wrong_login(self, client):
        response = client.get('/login')
        assert response.status_code == 200

        # Extract the CSRF token from the HTML content
        csrf_token = None
        content = response.data.decode('utf-8')
        token_start = content.find('name="csrf_token"') + len('name="csrf_token"') + 1
        token_end = content.find('>', token_start)
        csrf_token = content[token_start:token_end - 1]
        csrf_token_element = re.search(r'<input.*?id="csrf_token".*?>', content)
        if csrf_token_element:
            csrf_token_value = re.search(r'value="(.*?)"', csrf_token_element.group()).group(1)

        response = client.post('/login', data={
            'email': 'test@test.com',
            'password': 'wrongpassword',
            'remember': False,
            'submit': True,
            'csrf_token': csrf_token_value
        }, follow_redirects=True)

        assert b'Login Unsuccessful. Please check email and password' in response.data
        assert b'<title>Flask Task - Login</title>' in response.data
