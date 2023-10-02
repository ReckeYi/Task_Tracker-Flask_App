from flask import Blueprint, render_template, redirect, url_for, flash, Response

from flask_task import db, create_app
from flask_task.models import Role, Status, User, Project, Task

from faker import Faker
from faker.providers import DynamicProvider

dummy_data = Blueprint('dummy_data', __name__)


@dummy_data.route('/dummy')
def add_dummy_data() -> Response:
    fake_data = Faker()

    role_provider = DynamicProvider(
        provider_name='role_id',
        elements=[1, 2, 3]
    )
    fake_data.add_provider(role_provider)

    status_provider = DynamicProvider(
        provider_name='status_id',
        elements=[1, 2, 3, 4]
    )
    fake_data.add_provider(status_provider)

    user_provider = DynamicProvider(
        provider_name='user_id',
        elements=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    )
    fake_data.add_provider(user_provider)

    project_provider = DynamicProvider(
        provider_name='project_id',
        elements=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    )
    fake_data.add_provider(project_provider)

    roles = Role.query.all()
    if roles:
        flash('Database is not empty! You can add Dummy Data only once!', 'danger')
    else:
        role_1 = Role('admin')
        db.session.add(role_1)
        role_2 = Role('manager')
        db.session.add(role_2)
        role_3 = Role('user')
        db.session.add(role_3)
        db.session.commit()

        statuses = Status.query.all()
        if not statuses:
            status_1 = Status("To Do")
            db.session.add(status_1)
            status_2 = Status("In Progress")
            db.session.add(status_2)
            status_3 = Status("Done")
            db.session.add(status_3)
            status_4 = Status("Closed")
            db.session.add(status_4)
            db.session.commit()

        users = User.query.all()
        if not users:
            for _ in range(20):
                user = User(username=fake_data.unique.first_name(),
                            email=fake_data.unique.email(),
                            password=fake_data.password(),
                            role_id=fake_data.role_id())
                db.session.add(user)
            db.session.commit()

        projects = Project.query.all()
        if not projects:
            for _ in range(15):
                project = Project(title=fake_data.bothify(text='Project_##'),
                                  description=fake_data.text(300),
                                  user_id=fake_data.user_id())
                db.session.add(project)
            db.session.commit()

        tasks = Task.query.all()
        if not tasks:
            for _ in range(50):
                task = Task(title=fake_data.bothify(text='Task_##'),
                            description=fake_data.text(300),
                            user_id=fake_data.user_id(),
                            project_id=fake_data.project_id(),
                            deadline=fake_data.date_time(),
                            status_id=fake_data.status_id())
                db.session.add(task)
            db.session.commit()
        flash('Dummy data has been added to you data base!', 'success')
    return redirect(url_for('main.home'))
