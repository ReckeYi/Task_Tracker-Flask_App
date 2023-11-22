from flask_task import create_test_app
from flask_task.models import Project

app = create_test_app()


class TestProjectList:
    def test_project_list(self, client, login):
        response = client.get('/project_list')
        assert response.status_code == 200

        response_2 = client.post(
            '/project_list',
            data={
                'page_number': 1,
                'submit': True,
                'searched': 'test project',
                'search_submit': True,
            }
        )
        assert b'Test Project' in response_2.data


class TestNewProject:
    def test_new_project(self, client, login):
        response = client.post(
            '/project/new',
            data={
                'title': 'Test_Project_new_project',
                'description': 'Description of a project',
                'reporter': 1,
                'submit': True
            },
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b'New Project has been created!' in response.data
        assert b'<title>Flask Task - All Projects</title>' in response.data

        with app.app_context():
            new_project = Project.query.filter_by(title='Test_Project_new_project').first()
            assert new_project is not None


class TestProject:
    def test_project(self, client, login):
        with app.app_context():
            project = Project.query.filter_by(title='Test Project').first()
        response = client.get('/project/' + str(project.id))
        assert bytes(project.title, 'utf-8') in response.data


class TestUpdateProject:
    def test_update_project(self, client, login):
        with app.app_context():
            project = Project.query.filter_by(title='Test Project2').first()
        response = client.post(
            '/project/' + str(project.id) + '/update',
            data={
                'title': 'Updated Project2',
                'description': 'Description of a project',
                'reporter': 1,
                'submit': True
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b'Your project has been updated!' in response.data
        assert bytes(project.title, 'utf-8') not in response.data

        with app.app_context():
            project_updated = Project.query.filter_by(title='Updated Project2').first()
        response_2 = client.get(
            '/project/' + str(project_updated.id) + '/update')

        assert response_2.status_code == 200
        assert bytes(project_updated.title, 'utf-8') in response_2.data
        assert project_updated.title != project.title


class TestDeleteProject:
    def test_delete_project(self, client, login):
        with app.app_context():
            project = Project.query.filter_by(id=3).first()
        response = client.post(
            '/project/' + str(project.id) + '/delete',
            follow_redirects=True
        )
        assert b'Your project has been deleted!' in response.data
        assert b'<title>Flask Task - All Projects</title>'
        assert client.get('/project/' + str(project.id)).status_code == 404
