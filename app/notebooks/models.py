from app import db

class Notebook(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    order = db.Column(db.Integer, nullable=False, default=0)
    tasks = db.relationship('Task', backref='notebook', lazy=True, cascade='all, delete-orphan')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.String(300), nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    order = db.Column(db.Integer, nullable=False, default=0)
    notebook_id = db.Column(db.Integer, db.ForeignKey('notebook.id'), nullable=False)
