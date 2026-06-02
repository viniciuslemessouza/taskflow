from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('main/index.html')

@main.route('/terms')
def terms():
    return render_template('main/terms.html', title="Terms and Conditions")

@main.route('/notebooks')
def notebooks():
    return render_template('main/notebooks.html')