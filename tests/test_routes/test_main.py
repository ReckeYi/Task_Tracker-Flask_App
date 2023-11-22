from flask_task import create_test_app
from flask_task.models import User, Task, Project

app = create_test_app()
class TestMain:
    def test_main(self, client):
        with app.app_context():
            users_total = User.query.count()
            tasks_total = Task.query.count()
            projects_total = Project.query.count()
        assert client.get('/home').status_code == 200
        assert b'<title>Flask Task</title>' in client.get('/home').data
        assert b'<h1>Flask Task - Home Page</h1>' in client.get('/home').data
        assert users_total is not None
        assert tasks_total is not None
        assert projects_total is not None