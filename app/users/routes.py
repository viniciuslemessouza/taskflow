from flask import Blueprint, render_template, redirect, flash
from app.users.forms import LoginForm, RegisterForm

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

@users.route('/account')
def account():
    return render_template('users/account.html', title="Account")

@users.route('/logout')
def logout():
    return redirect('home')