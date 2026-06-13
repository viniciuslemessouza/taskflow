import app.users.utils
from app import bcrypt, db
from app.users.models import User
from flask_login import login_user, login_required, logout_user
from flask import Blueprint, render_template, redirect, flash, url_for
from app.users.forms import LoginForm, RegisterForm, AccountForm, PasswordRecoveryForm, SetNewPassword

users = Blueprint("users", __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember)
            flash('Logged In', 'success')
            return redirect(url_for('notebooks.get_notebooks'))
        else:
            flash('Please check password and email.', 'warning')
    return render_template('users/login.html', title="Login", form=form)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(email=form.email.data, password=hashed_password, terms_agreement=form.terms.data)
        db.session.add(user)
        db.session.commit()
        flash("You're now registered. Please log in.", 'success')
        return redirect(url_for('users.login'))
    else:
        return render_template('users/register.html', title="Register", form=form)

@users.route('/password_recovery', methods=['GET', 'POST'])
def password_recovery():
    form = PasswordRecoveryForm()
    if form.validate_on_submit():
        return redirect(url_for('main.home'))
    else:
        return render_template('users/password_recovery.html', title="Password Recovery", form=form)

@users.route('/set_new_password', methods=['GET', 'POST'])
def set_new_password():
    form = SetNewPassword()
    if form.validate_on_submit():
        return redirect(url_for('notebooks.get_notebooks'))
    else:
        return render_template('users/new_password.html', title="New Password", form=form)

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    return render_template('users/account.html', title="Account", form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect('home')