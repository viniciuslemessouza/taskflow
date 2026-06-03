from flask import Blueprint, render_template
from app.notebooks.forms import NewNotebookForm

notebooks = Blueprint('notebooks', __name__)

@notebooks.route('/notebooks')
def get_notebooks():
    form = NewNotebookForm()
    return render_template('notebooks/notebooks.html', form=form)

@notebooks.route('/notebook/<notebook_id>')
def get_notebook(notebook_id):
    form = NewNotebookForm()
    return render_template('notebooks/notebook.html', form=form)