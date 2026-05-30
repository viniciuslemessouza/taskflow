from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.main.routes import main
    from app.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app