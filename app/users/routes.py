from flask import Blueprint, render_template, redirect, flash
from app.users.forms import LoginForm

users = Blueprint("users", __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('home')
    else:
        return render_template('users/login.html', title="Login", form=form)

@users.route('/register')
def register():
    return render_template('users/register.html', title="Register")

@users.route('/account')
def account():
    return render_template('users/account.html', title="Account")

@users.route('/logout')
def logout():
    return redirect('home')