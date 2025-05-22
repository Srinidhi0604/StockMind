from functools import wraps
from flask import session, render_template

# login required decorator for API routes
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            return render_template("FRONT.html", error="Please log in to continue.")
        return f(*args, **kwargs)
    return decorated
