import requests
import math

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def time(time):
    """Format time"""
    hours = math.floor(time / 3600)
    minutes = math.floor(time / 60)
    seconds = time % 60
    if seconds < 10:
        seconds = f"0{seconds}"

    if hours > 0:
        if minutes < 10:

            minutes = f"0{minutes}"

        return f"{hours}:{minutes}:{seconds}"

    else:
        return f"{minutes}:{seconds}"
        
def url(url):
    url = url.replace("-", " ")
    return url
