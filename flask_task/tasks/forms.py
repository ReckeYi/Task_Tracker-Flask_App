from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=40)])
    description = TextAreaField('Description', validators=[Length(min=2, max=500)])
    project_id = SelectField('Project', choices=[], coerce=int)
    deadline = DateField('Deadline', format='%Y-%m-%d')
    status_id = SelectField('Status', choices=[], coerce=int)
    assignee = SelectField('Assignee', choices=[], coerce=int)
    submit = SubmitField('Submit')
