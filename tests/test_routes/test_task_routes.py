from datetime import datetime

from flask_task import create_test_app
from flask_task.models import Task, Project

app = create_test_app()
class TestNewTask:
    def test_new_task(self, client, login):
        response = client.post(
            '/task/new',
            data = {
                'title': 'Test Task New',
                'description': 'Task Description',
                'project_id': '1',
                'deadline': '2024-01-01',
                'status_id': '1',
                'assignee': '1',
                'submit': True
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b'New Task has been created!' in response.data
        with app.app_context():
            new_task = Task.query.filter_by(title='Test Task New').first()
        assert new_task is not None
        assert new_task.title == 'Test Task New'
        assert new_task.description == 'Task Description'

    def test_new_task_unauthenticated(self, client):
        response = client.post(
            '/task/new',
            data = {
                'title': 'Test2 Task New',
                'description': 'Task Description',
                'project_id': '1',
                'deadline': '2024-01-01',
                'status_id': '2',
                'assignee': '1',
                'submit': True
            },
            follow_redirects=True
        )
        with app.app_context():
            new_task = Task.query.filter_by(title='Test2 Task New').first()
        assert new_task is None
        assert b'New Task has been created!' not in response.data

class TestAddTaskToCurrentProject:
    def test_add_task_to_current_project(self, client, login):
        with app.app_context():
            project = Project.query.filter_by(title='Test Project').first()
        response = client.post(
            '/task/add/' + str(project.id),
            data={
                'title': 'Test Task2 New',
                'description': 'Task Description',
                'project_id': '1',
                'deadline': '2024-01-01',
                'status_id': '1',
                'assignee': '1',
                'submit': True
            },
            follow_redirects=True
        )
        assert b'New Task has been created!' in response.data
        assert bytes(project.title, 'utf-8') in response.data
        assert b'<title>Flask Task - New Task</title>'


class TestTask:
    def test_task(self, client, login):
        with app.app_context():
            task = Task.query.filter_by(id=1).first()
        response = client.get('/task/' + str(task.id))
        assert response.status_code == 200
        assert bytes(task.title, 'utf8') in response.data

    def test_task_invalid_task_id(self, client, login):
        response = client.get('/task/1230')
        assert response.status_code == 404


class TestUpdateTask:
    def test_update_task_post_method(self, client, login):
        with app.app_context():
            task = Task.query.filter_by(title='Test Task 2').first()
        response = client.post(
            '/task/' + str(task.id) + '/update',
            data={
                'title': 'Test2 Task New Updated',
                'description': 'Task Description',
                'project_id': '1',
                'deadline': '2024-01-01',
                'status_id': '2',
                'assignee': '1',
                'submit': True
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b'Your task has been updated!'
        with app.app_context():
            task_updated = task = Task.query.filter_by(title='Test2 Task New Updated').first()
        assert bytes(task_updated.title, 'utf8') in response.data
        assert client.get('/task/' + str(task_updated.id) + '/update').status_code == 200

class TestDeleteTask:
    def test_delete_task(self, client, login):
        with app.app_context():
            task = Task.query.filter_by(title='Test Task 3').first()
        response = client.post('/task/' + str(task.id) + '/delete', follow_redirects = True)
        assert b'Your task has been deleted!' in response.data
        assert b'<title>Flask Task - Home</title>'

    def test_delete_task_invalid_task_id(self, client, login):
        assert client.post('/task/3265/delete').status_code == 404
