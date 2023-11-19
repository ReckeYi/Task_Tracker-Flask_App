from flask_task import create_test_app
from flask_task.models import User

app = create_test_app()


class TestViews:

    def test_home(self, client):
        assert client.get('/home').status_code == 200
        assert client.get('/').status_code == 200

    def test_register(self, client):
        assert client.get('/register').status_code == 200

    def test_login(self, client):
        assert client.get('/login').status_code == 200

    def test_404(self, client):
        assert client.get('/this_page_would_not_be_exist').status_code == 404

    def test_project_list(self, client):
        assert client.get('/project_list').status_code == 302

    def test_project_list_user_is_authenticated(self, login, client):
        with app.app_context():
            assert client.get('/project_list').status_code == 200

    def test_users(self, client):
        assert client.get('/users').status_code == 302

    def test_users_user_is_authenticated(self, login, client):
        with app.app_context():
            assert client.get('/users').status_code == 200

    def test_user_tasks_username(self, client):
        assert client.get('/user/tasks/oleg').status_code == 302

    def test_user_tasks_username_user_is_authenticated(self, login, client):
        with app.app_context():
            user = User.query.filter_by(username='test').first()
            username = user.username
            assert client.get('/user/tasks/' + username).status_code == 200

    def test_task_new(self, client):
        assert client.get('/task/new').status_code == 302

    def test_task_new_user_is_authenticated(self, login, client):
        with app.app_context():
            assert client.get('/task/new').status_code == 200

    def test_project_new(self, client):
        assert client.get('/project/new').status_code == 302

    def test_project_user_is_authenticated(self, login, client):
        with app.app_context():
            assert client.get('/account').status_code == 200

    def test_account(self, client):
        assert client.get('/account').status_code == 302

    def test_account_is_authenticated(self, login, client):
        with app.app_context():
            assert client.get('/project/new').status_code == 200

    def test_logout(self, client):
        assert client.get('/logout').status_code == 302

    def test_logout_is_authenticated(self, login, client):
        with app.app_context():
            assert client.get('/logout').status_code == 302
            assert client.get('/account').status_code == 302
            assert client.get('/home').status_code == 200

