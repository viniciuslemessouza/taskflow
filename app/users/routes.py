from flask import Blueprint, render_template, redirect

users = Blueprint("users", __name__)

@users.route('/login')
def login():
    return render_template('users/login.html', title="Login")

@users.route('/register')
def register():
    return render_template('users/register.html', title="Register")

@users.route('/account')
def account():
    return render_template('users/account.html', title="Account")

@users.route('/logout')
def logout():
    return redirect('home')