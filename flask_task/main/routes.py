from flask import Blueprint, render_template, request

from flask_task.models import Project, Task, User

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home() -> str:
    users_total = User.query.count()
    tasks_total = Task.query.count()
    projects_total = Project.query.count()
    return render_template('home.html',
                           users_total=users_total,
                           tasks_total=tasks_total,
                           projects_total=projects_total)
