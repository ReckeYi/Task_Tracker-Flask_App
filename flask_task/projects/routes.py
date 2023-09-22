from flask import Blueprint, flash, redirect, render_template, url_for, request, abort
from flask_login import login_required, current_user

from flask_task.models import User, Project, Task
from flask_task.projects.forms import ProjectForm, PerPageForm, SearchForm
from flask_task import db

projects = Blueprint('projects', __name__)


@projects.route("/project_list", methods=['GET', 'POST'])
@login_required
def project_list():
    form = PerPageForm()
    form2 = SearchForm()
    page = request.args.get('page', 1, type=int)
    per_page = form.page_number.data
    if not per_page:
        per_page = request.args.get('page_number', 3, type=int)
    searched = request.args.get('searched')
    if searched:
        per_page = form.page_number.data
        form2.searched.data = searched
        projects = Project.query.filter(Project.title.ilike('%' + searched + '%') |
                                        Project.description.ilike('%' + searched + '%')).paginate(page=page,
                                                                                                  per_page=per_page)
        return render_template('project_list.html', projects=projects, form=form, form2=form2)
    else:
        form.page_number.data = per_page
        projects = Project.query.order_by(Project.title).paginate(page=page, per_page=per_page)
        return render_template('project_list.html', projects=projects, form=form, form2=form2)


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
        return redirect(url_for('projects.project_list'))
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
