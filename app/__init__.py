from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    from app.main.routes import main
    from app.users.routes import users
    from app.notebooks.routes import notebooks

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(notebooks)

    return app