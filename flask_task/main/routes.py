from flask import Blueprint, render_template, request

from flask_task.models import Project

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    projects = Project.query.order_by(Project.title).paginate(page=page, per_page=10)
    return render_template('home.html', projects=projects)