from app.notebooks.models import Notebook, Task
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, abort
from app.notebooks.forms import NewNotebookForm, NewTaskForm

notebooks = Blueprint('notebooks', __name__)

@notebooks.route('/notebooks')
@login_required
def get_notebooks():
    form = NewNotebookForm()
    page = request.args.get('page', 1, type=int)
    user_notebooks = Notebook.query.filter_by(user_id=current_user.id).order_by(Notebook.id.desc()).paginate(page=page, per_page=12)
    return render_template('notebooks/notebooks.html', form=form, notebooks=user_notebooks)

@notebooks.route('/notebook/<notebook_id>')
@login_required
def get_notebook(notebook_id):
    form = NewTaskForm()
    user_notebook = Notebook.query.get_or_404(notebook_id)
    if user_notebook.user != current_user:
        abort(403)

    tasks = Task.query.filter_by(notebook_id=user_notebook.id).order_by(Task.id.desc()).all()
    return render_template('notebooks/notebook.html', form=form, tasks=tasks, notebook_title=user_notebook.title)