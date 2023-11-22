from flask import Blueprint, flash, redirect, render_template, url_for, request, abort
from flask_login import login_required, current_user

from flask_task import db
from flask_task.models import Project, Status, User, Task
from flask_task.tasks.forms import TaskForm, ProjectTaskForm

from werkzeug import Response
from typing import Union, Any

tasks = Blueprint('tasks', __name__)


@tasks.route("/task/new", methods=['GET', 'POST'])
@login_required
def new_task() -> Union[Response, str]:
    projects = Project.query.all()
    project_list = [(i.id, i.title) for i in projects]
    statuses = Status.query.all()
    status_list = [(i.id, i.status) for i in statuses]
    users = User.query.all()
    users_list = [(i.id, i.username) for i in users]
    form = TaskForm()
    form.project_id.choices = project_list
    form.status_id.choices = status_list
    form.assignee.choices = users_list
    if form.validate_on_submit():
        task_new = Task(title=form.title.data, description=form.description.data, user_id=current_user.id,
                        project_id=form.project_id.data, deadline=form.deadline.data, status_id=form.status_id.data)
        db.session.add(task_new)
        db.session.commit()
        flash('New Task has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_task.html', title='New Task', form=form, legend='New Task')


@tasks.route("/task/add/<int:project_id>", methods=['GET', 'POST'])
@login_required
def add_task_to_current_project(project_id: int) -> Union[Response, str]:
    project = Project.query.get_or_404(project_id)
    projects = Project.query.all()
    project_list = [(i.id, i.title) for i in projects]
    statuses = Status.query.all()
    status_list = [(i.id, i.status) for i in statuses]
    users = User.query.all()
    users_list = [(i.id, i.username) for i in users]
    form = ProjectTaskForm()
    form.project_id.choices = project_list
    form.status_id.choices = status_list
    form.assignee.choices = users_list
    if form.validate_on_submit():
        add_task = Task(title=form.title.data, description=form.description.data, user_id=current_user.id,
                        project_id=form.project_id.data, deadline=form.deadline.data, status_id=form.status_id.data)
        db.session.add(add_task)
        db.session.commit()
        flash('New Task has been created!', 'success')
        return redirect(url_for('projects.project', project_id=form.project_id.data))
    elif request.method == 'GET':
        form.project_id.data = project.id
    return render_template('create_task.html', title='New Task', form=form, project=project, legend='New Task')


@tasks.route("/task/<int:task_id>", methods=['GET'])
def task(task_id: int) -> int:
    task_q = Task.query.get_or_404(task_id)
    return render_template('task.html', title=task_q.title, task=task_q)


@tasks.route("/task/<int:task_id>/update", methods=['GET', 'POST'])
@login_required
def update_task(task_id: Any) -> Union[Response, str]:
    projects = Project.query.all()
    project_list = [(i.id, i.title) for i in projects]
    statuses = Status.query.all()
    status_list = [(i.id, i.status) for i in statuses]
    users = User.query.all()
    users_list = [(i.id, i.username) for i in users]
    task_q = Task.query.get_or_404(task_id)
    if current_user.role_id != 1:
        abort(403)
    form = TaskForm()
    form.project_id.choices = project_list
    form.status_id.choices = status_list
    form.assignee.choices = users_list
    if form.validate_on_submit():
        task_q.title = form.title.data
        task_q.description = form.description.data
        task_q.project_id = form.project_id.data
        task_q.deadline = form.deadline.data
        task_q.status_id = form.status_id.data
        task_q.user_id = form.assignee.data
        db.session.commit()
        flash('Your task has been updated!', 'success')
        return redirect(url_for('tasks.task', task_id=task_q.id))
    elif request.method == 'GET':
        form.title.data = task_q.title
        form.description.data = task_q.description
        form.project_id.data = task_q.project_id
        form.deadline.data = task_q.deadline
        form.status_id.data = task_q.status_id
        form.assignee.data = task_q.user_id
    return render_template('create_task.html', title='Update Task', form=form, legend='Update Task')


@tasks.route("/task/<int:task_id>/delete", methods=['POST'])
@login_required
def delete_task(task_id: int) -> Response:
    task_q = Task.query.get_or_404(task_id)
    if current_user.role_id != 1:
        abort(403)
    db.session.delete(task_q)
    db.session.commit()
    flash('Your task has been deleted!', 'success')
    return redirect(url_for('main.home'))
