from functools import wraps

from flask import render_template, redirect, url_for, request, g

def login_required(f):
    """Decorator which redirects to login if the
       user is not logged in.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None or not g.user.is_authenticated():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

