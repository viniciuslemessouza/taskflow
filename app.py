from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    button = {'href': 'login', 'text': 'Login'}
    return render_template('index.html', button=button)

@app.route('/login')
def login():
    button = {'href': 'register', 'text': 'Register'}
    return render_template('login.html', title='Login', button=button)

@app.route('/register')
def register():
    button = {'href': 'login', 'text': 'Login'}
    return render_template('register.html', title='Register', button=button)

@app.route('/checklist')
def checklist():
    button = {'href': 'login', 'text': 'Login'}
    return render_template('checklist.html', title='Checklist', button=button)

@app.route('/terms')
def terms():
    button = {'href': 'login', 'text': 'Login'}
    return render_template('terms.html', title='Terms', button=button)

@app.route('/password_recovery')
def password_recovery():
    button = {'href': 'login', 'text': 'Login'}
    return render_template('password_recovery.html', title='Recovery', button=button)

if __name__ == '__main__':
    app.run(debug=True)