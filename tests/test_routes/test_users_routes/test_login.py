import pytest


class TestLogin:
    def test_login(self, client):
        '''This piece of code is required for testing with CSRF'''
        # response = client.get('/login')
        # assert response.status_code == 200

        # # Extract the CSRF token from the HTML content
        # csrf_token = None
        # content = response.data.decode('utf-8')
        # token_start = content.find('name="csrf_token"') + len('name="csrf_token"') + 1
        # token_end = content.find('>', token_start)
        # csrf_token = content[token_start:token_end - 1]
        # csrf_token_element = re.search(r'<input.*?id="csrf_token".*?>', content)
        # if csrf_token_element:
        #     csrf_token_value = re.search(r'value="(.*?)"', csrf_token_element.group()).group(1)

        response = client.post(
            '/login',
            data={
                'email': 'test@test.com',
                'password': 'test',
                'remember': True,
                'submit': True,
                # 'csrf_token': csrf_token_value
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b'<h1>Flask Task - Home Page</h1>' in response.data
        assert client.get('/login').status_code == 302
        assert client.get('/project_list').status_code == 200

    def test_login_invalid_email(self, client):
        response = client.post(
            '/login',
            data={
                'email': 'wrongtest@test.com',
                'password': 'test',
                'remember': False,
                'submit': True,
            },
            follow_redirects=True
        )

        assert b'Login Unsuccessful. Please check email and password' in response.data
        assert b'<title>Flask Task - Login</title>' in response.data

    def test_login_invalid_password(self, client):
        response = client.post(
            '/login',
            data={
                'email': 'test2@test.com',
                'password': 'wrongpassword',
                'remember': False,
                'submit': True,
            },
            follow_redirects=True
        )

        assert b'Login Unsuccessful. Please check email and password' in response.data
        assert b'<title>Flask Task - Login</title>' in response.data
