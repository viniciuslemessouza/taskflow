from flask_wtf import FlaskForm
from app.users.models import User
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, ValidationError

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    terms = BooleanField('terms', validators=[DataRequired('You need to agree with our terms.')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f'"{self.email.data}" is already in use!')

class AccountForm(FlaskForm):
    fullname = StringField('Full name', validators=[Length(min=8, max=150)])
    email = EmailField('Email', validators=[Email()])
    profile_picture = FileField('Profile picture', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    submit = SubmitField('Update')

class PasswordRecoveryForm(FlaskForm):
    email = EmailField('Email', validators=[Email()])
    submit = SubmitField('Submit')

class SetNewPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')