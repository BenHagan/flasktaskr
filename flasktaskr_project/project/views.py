# views.py

from project import app, db
from flask import flash, redirect, session, url_for, render_template
from functools import wraps

# helper functions
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % \
                (getattr(form, field).label.text, error), 'error')

# routes
@app.route('/', defaults={'page': 'index'})
def index(page):
    return redirect(url_for('tasks.tasks'))

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500