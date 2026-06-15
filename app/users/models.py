from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False, default='Fullname')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    terms_agreement = db.Column(db.Boolean, nullable=False, default=False)
    profile_picture = db.Column(db.String(20), nullable=False, default="default.png")
    notebooks = db.relationship("Notebook", backref="user", lazy=True)