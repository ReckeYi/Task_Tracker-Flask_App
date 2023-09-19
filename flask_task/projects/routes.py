from flask import Blueprint, flash, redirect, render_template, url_for, request, abort
from flask_login import login_required, current_user

from flask_task.models import User, Project, Task
from flask_task.projects.forms import ProjectForm
from flask_task import db

projects = Blueprint('projects', __name__)


@projects.route('/project_list')
def project_list():
    page = request.args.get('page', 1, type=int)
    projects = Project.query.order_by(Project.title).paginate(page=page, per_page=5)
    return render_template('project_list.html', projects=projects)

@projects.route("/project/new", methods=['GET', 'POST'])
@login_required
def new_project():
    users = User.query.all()
    users_list = [(i.id, i.username) for i in users]
    form = ProjectForm()
    form.reporter.choices = users_list
    if form.validate_on_submit():
        project = Project(title=form.title.data, description=form.description.data, user_id=form.reporter.data)
        db.session.add(project)
        db.session.commit()
        flash('New Project has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_project.html', title='New Project', form=form, legend='New Project')


@projects.route("/project/<int:project_id>", methods=['GET', 'POST'])
def project(project_id):
    project = Project.query.get_or_404(project_id)
    tasks = Task.query.filter_by(project_id=project.id).all()
    return render_template('project.html', title=project.title, project=project, tasks=tasks)


@projects.route("/project/<int:project_id>/update", methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    users = User.query.all()
    users_list = [(i.id, i.username) for i in users]
    project = Project.query.get_or_404(project_id)
    # if project.user_id != current_user.id:
    if current_user.role_id != 1:
        abort(403)
    form = ProjectForm()
    form.reporter.choices = users_list
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.user_id = form.reporter.data
        db.session.add(project)
        db.session.commit()
        flash('Your project has been updated!', 'success')
        return redirect(url_for('projects.project', project_id=project.id))
    elif request.method == 'GET':
        form.title.data = project.title
        form.description.data = project.description
        form.reporter.data = project.user_id
    return render_template('create_project.html', title='Update Project', form=form, legend='Update Project')


@projects.route("/project/<int:project_id>/delete", methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    # if project.user_id != current_user.id:
    if current_user.role_id != 1:
        abort(403)
    db.session.delete(project)
    db.session.commit()
    flash('Your project has been deleted!', 'success')
    return redirect(url_for('main.home'))