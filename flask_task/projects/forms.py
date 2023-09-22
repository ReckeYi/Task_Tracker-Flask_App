from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange


class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=40)])
    description = TextAreaField('Description', validators=[Length(min=2, max=300)])
    reporter = SelectField('Reporter', choices=[], coerce=int)
    submit = SubmitField('Submit')


class PerPageForm(FlaskForm):
    page_number = SelectField(u'Per Page', choices=[2, 5, 10, 15, 20, 50], coerce=int)
    submit = SubmitField('Confirm')

class SearchForm(FlaskForm):
    searched = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Searchhh')

