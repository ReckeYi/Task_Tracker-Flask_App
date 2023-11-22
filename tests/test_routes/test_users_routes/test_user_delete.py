from flask_task import create_test_app
from flask_task.models import User

app = create_test_app()


class TestDeleteUser:
    def test_update_account_valid(self, client, login):
        with app.app_context():
            user = User.query.filter_by(username='test3').first()
            response = client.post('/user/' + str(user.id) + '/delete', follow_redirects=True)
            deleted_user = User.query.filter_by(username='test3').first()
            assert deleted_user is None
            assert b'User has been deleted!' in response.data

    def test_update_account_invalid_id(self, client, login):
        with app.app_context():
            response = client.post('/user/' + str(204) + '/delete', follow_redirects=True)
            assert response.status_code == 404
            assert b'That page does not exist. Please try a different location' in response.data
