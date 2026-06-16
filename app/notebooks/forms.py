from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NewNotebookForm(FlaskForm):
    title = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('check')

class NewTaskForm(FlaskForm):
    content = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('check')