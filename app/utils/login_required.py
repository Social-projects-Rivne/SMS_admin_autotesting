from functools import wraps

from flask import session, url_for, request, redirect


def login_required(rout):
    """decorator which redirect to page login
       in case if user is not authenticated
    """
    @wraps(rout)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return rout(*args, **kwargs)
    return decorated_function