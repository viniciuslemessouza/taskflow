from flask import Blueprint, render_template, redirect, flash
from app.users.forms import LoginForm, RegisterForm, AccountForm, PasswordRecoveryForm, SetNewPassword

users = Blueprint("users", __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('home')
    else:
        return render_template('users/login.html', title="Login", form=form)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect('home')
    else:
        return render_template('users/register.html', title="Register", form=form)

@users.route('/password_recovery', methods=['GET', 'POST'])
def password_recovery():
    form = PasswordRecoveryForm()
    if form.validate_on_submit():
        return redirect('home')
    else:
        return render_template('users/password_recovery.html', title="Password Recovery", form=form)

@users.route('/set_new_password', methods=['GET', 'POST'])
def set_new_password():
    form = SetNewPassword()
    if form.validate_on_submit():
        return redirect('home')
    else:
        return render_template('users/new_password.html', title="Password Recovery", form=form)

@users.route('/account', methods=['GET', 'POST'])
def account():
    form = AccountForm()
    return render_template('users/account.html', title="Account", form=form)

@users.route('/logout')
def logout():
    return redirect('home')