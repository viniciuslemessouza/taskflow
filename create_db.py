import secrets
from flask import Flask
from config import Config
from app import db

app = Flask(__name__)
app.config.from_object(Config)

from app.users.models import User
from app.notebooks.models import Notebook, Task

db.init_app(app)

def create_user():
    user1 = User(fullname='Vinicius Lemes de Souza', email='viniciuslemes314@gmail.com', password=secrets.token_hex(8),
                 terms_agreement=True, profile_picture='default.png')
    user2 = User(fullname='Debora Barbara Viana Alves da Silva', email='deborabvas@gmail.com',
                 password=secrets.token_hex(8), terms_agreement=True, profile_picture='default.png')
    user3 = User(fullname='Vinicius Lemes de Souza', email='viniciuslemes31415@gmail.com',
                 password=secrets.token_hex(8), terms_agreement=True, profile_picture='default.png')
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

def create_notebook(index, user_id):
    notebook = Notebook(title=f"Notebook {index}", user_id=user_id)
    db.session.add(notebook)

def create_task(index, notebook_id):
    task = Task(content=f"Task {index}", notebook_id=notebook_id)
    db.session.add(task)

with app.app_context():
    db.create_all()
    create_user()
    for user_index in range(1, 4):
        for notebook_index in range(1, 101):
            create_notebook(notebook_index, user_index)
            for task_index in range(1, 101):
                create_task(task_index, notebook_index)
    db.session.commit()
