from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length
from wtforms import EmailField, PasswordField, BooleanField, SubmitField

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Submit')