from flask import Blueprint, render_template, request

from flask_task.models import Project

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')
