from app import db
from app.notebooks.models import Notebook, Task
from flask_login import current_user, login_required
from app.notebooks.forms import NewNotebookForm, NewTaskForm
from flask import Blueprint, render_template, request, abort, redirect, url_for

notebooks = Blueprint('notebooks', __name__)

@notebooks.route('/notebooks', methods=['GET', 'POST'])
@login_required
def get_notebooks():
    form = NewNotebookForm()
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        new_notebooks = request.form.getlist('new_notebooks')
        deleted_notebooks = request.form.getlist('deleted_notebooks')
        for title in reversed(new_notebooks):
            title = title.strip()
            if title:
                db.session.add(Notebook(title=title, user_id=current_user.id))
        for notebook_id in deleted_notebooks:
            notebook = Notebook.query.filter_by(id=notebook_id, user_id=current_user.id).first()
            if notebook:
                db.session.delete(notebook)
        db.session.commit()
        return redirect(url_for('notebooks.get_notebooks', page=page))
    user_notebooks = Notebook.query.filter_by(user_id=current_user.id).order_by(Notebook.id.desc()).paginate(page=page, per_page=12)
    for notebook in user_notebooks.items:
        total_tasks = Task.query.filter_by(notebook_id=notebook.id).count()
        completed_tasks = Task.query.filter_by(notebook_id=notebook.id, status=True).count()
        notebook.progress = round((completed_tasks / total_tasks) * 100) if total_tasks else 0
    return render_template('notebooks/notebooks.html', form=form, notebooks=user_notebooks)

@notebooks.route('/notebook/<int:notebook_id>', methods=['GET', 'POST'])
@login_required
def get_notebook(notebook_id):
    form = NewTaskForm()
    user_notebook = Notebook.query.get_or_404(notebook_id)
    if user_notebook.user != current_user:
        abort(403)
    if request.method == 'POST':
        new_tasks = request.form.getlist('new_tasks')
        deleted_tasks = request.form.getlist('deleted_tasks')
        task_order = request.form.getlist('task_order')
        task_status = request.form.getlist('task_status')
        for task_content in reversed(new_tasks):
            task_content = task_content.strip()
            if task_content:
                db.session.add(Task(content=task_content, notebook_id=user_notebook.id, status=False, order=0))
        for index, task_id in enumerate(task_order):
            task = Task.query.filter_by(id=task_id, notebook_id=user_notebook.id).first()
            if task:
                task.order = index
        for status_data in task_status:
            task_id, status = status_data.split(':')
            task = Task.query.filter_by(id=task_id, notebook_id=user_notebook.id).first()
            if task:
                task.status = status == '1'
        for task_id in deleted_tasks:
            task = Task.query.filter_by(id=task_id, notebook_id=user_notebook.id).first()
            if task:
                db.session.delete(task)
        db.session.commit()
        return redirect(url_for('notebooks.get_notebook', notebook_id=user_notebook.id))
    tasks = Task.query.filter_by(notebook_id=user_notebook.id).order_by(Task.order.asc(), Task.id.desc()).all()
    return render_template('notebooks/notebook.html', form=form, tasks=tasks,
                           notebook_title=user_notebook.title)

@notebooks.route('/task/<int:task_id>/status', methods=['POST'])
@login_required
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    if task.notebook.user != current_user:
        abort(403)
    task.status = request.form.get('status') == 'true'
    db.session.commit()
    return {'status': 'success', 'task_status': task.status}