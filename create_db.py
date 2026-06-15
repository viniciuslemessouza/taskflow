from flask import Flask
from config import Config
from app import db

app = Flask(__name__)
app.config.from_object(Config)

from app.users.models import User
from app.notebooks.models import Notebook, Task

db.init_app(app)

with app.app_context():
    db.create_all()
    for user_index in range(1, 4):
        for notebook_index in range(1, 101):
            notebook = Notebook(title=f"Notebook {notebook_index}", user_id=user_index)
            db.session.add(notebook)
            db.session.flush()
            for task_index in range(1, 101):
                task = Task(content=f"Task {task_index}", notebook_id=notebook.id)
                db.session.add(task)
    db.session.commit()
