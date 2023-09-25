from flask import Blueprint, redirect, url_for, flash, render_template, request, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug import Response

from flask_task import bcrypt, db
from flask_task.models import User, Role, Project, Task
from flask_task.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, UpdateUserForm, \
    RequestResetForm, ResetPasswordForm, AddUserForm
from flask_task.users.utils import save_picture, send_reset_email

from typing import Union

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register() -> Union[Response, str]:
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role_id=1)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    if current_user.role_id == 1:
        roles = Role.query.all()
        roles_list = [(i.id, i.role) for i in roles]
        form = UpdateAccountForm()
        form.role_id.choices = roles_list
    else:
        form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        if current_user.role_id == 1:
            current_user.role_id = form.role_id.data
        else:
            None
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.role_id.data = current_user.role_id
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route('/user/update/<string:username>', methods=['GET', 'POST'])
@login_required
def user_update(username):
    user = User.query.filter_by(username=username).first_or_404()
    roles = Role.query.all()
    roles_list = [(i.id, i.role) for i in roles]
    form = UpdateUserForm()
    form.role_id.choices = roles_list
    if current_user.role_id != 1:
        abort(403)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file
        user.username = form.username.data
        user.email = form.email.data
        user.role_id = form.role_id.data
        db.session.commit()
        flash('User account has been updated!', 'success')
        return redirect(url_for('users.users_list'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.role_id.data = user.role_id
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    return render_template('user_update.html', title='Update User', image_file=image_file, form=form, user=user)

@users.route("/user/<int:user_id>/delete", methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.role_id != 1:
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted!', 'success')
    return redirect(url_for('users.users_list'))


@users.route('/user/<string:username>')
@login_required
def user_projects(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    projects = Project.query.filter_by(user=user).order_by(Project.title).paginate(page=page, per_page=10)
    return render_template('user_projects.html', projects=projects, user=user)


@users.route('/user/<string:username>/<string:title>')
@login_required
def user_project_tasks(username, title):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    project = Project.query.filter_by(title=title).first_or_404()
    tasks = Task.query.filter_by(user=user, project=project).order_by(Task.title).paginate(page=page, per_page=10)
    return render_template('user_project_tasks.html', tasks=tasks, user=user, project=project)


@users.route('/user/tasks/<string:username>')
@login_required
def user_tasks(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    tasks = Task.query.filter_by(user=user).order_by(Task.title).paginate(page=page, per_page=10)
    if current_user.role_id != 1:
        abort(403)
    return render_template('user_tasks.html', tasks=tasks, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route('/users', methods=['GET'])
@login_required
def users_list():
    users = User.query
    if current_user.role_id != 1:
        abort(403)
    return render_template('users.html', title='All Users', users=users)

@users.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    roles = Role.query.all()
    roles_list = [(i.id, i.role) for i in roles]
    if current_user.role_id != 1:
        abort(403)
    form = AddUserForm()
    form.role_id.choices = roles_list
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    role_id=form.role_id.data)
        db.session.add(user)
        db.session.commit()
        flash('User has been created! You are now able to log in', 'success')
        return redirect(url_for('users.users_list'))
    return render_template('add_user.html', title='Register', form=form)

