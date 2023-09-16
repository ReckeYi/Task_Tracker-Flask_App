from flask import Blueprint, flash, redirect, render_template, url_for, request, abort
from flask_login import login_required, current_user

from flask_task import db
from flask_task.models import Project, Status, User, Task
from flask_task.tasks.forms import TaskForm

tasks = Blueprint('tasks', __name__)


@tasks.route("/task/new", methods=['GET', 'POST'])
@login_required
def new_task():
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
        task = Task(title=form.title.data, description=form.description.data, user_id=current_user.id,
                    project_id=form.project_id.data, deadline=form.deadline.data, status_id=form.status_id.data)
        db.session.add(task)
        db.session.commit()
        flash('New Task has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_task.html', title='New Task', form=form, legend='New Task')


@tasks.route("/task/<int:task_id>", methods=['GET', 'POST'])
def task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task.html', title=task.title, task=task)


@tasks.route("/task/<int:task_id>/update", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    projects = Project.query.all()
    project_list = [(i.id, i.title) for i in projects]
    statuses = Status.query.all()
    status_list = [(i.id, i.status) for i in statuses]
    users = User.query.all()
    users_list = [(i.id, i.username) for i in users]
    task = Task.query.get_or_404(task_id)
    # if task.user_id != current_user.id:
    if current_user.role_id != 1:
        abort(403)
    form = TaskForm()
    form.project_id.choices = project_list
    form.status_id.choices = status_list
    form.assignee.choices = users_list
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.project_id = form.project_id.data
        task.deadline = form.deadline.data
        task.status_id = form.status_id.data
        task.user_id = form.assignee.data
        db.session.commit()
        flash('Your task has been updated!', 'success')
        return redirect(url_for('tasks.task', task_id=task.id))
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.project_id.data = task.project_id
        form.deadline.data = task.deadline
        form.status_id.data = task.status_id
        form.assignee.data = task.user_id
    return render_template('create_task.html', title='Update Task', form=form, legend='Update Task')


@tasks.route("/task/<int:task_id>/delete", methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    # if task.user_id != current_user.id:
    if current_user.role_id != 1:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Your task has been deleted!', 'success')
    return redirect(url_for('main.home'))