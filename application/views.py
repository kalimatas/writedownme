from functools import wraps
from flask import render_template
from flask import request
from flask import redirect
from application import app

from google.appengine.api import users

def auth_required(aFunc):
    """Require login"""
    @wraps(aFunc)
    def _auth_wrapper(*args, **kwargs):
        if not users.get_current_user():
            return redirect(users.create_login_url(request.url))
        return aFunc(*args, **kwargs)
    return _auth_wrapper

def latest_ideas():
    """List of latest ideas"""
    return render_template('ideas_list.html')

@auth_required
def add_new_idea():
    """Create new idea"""

    # show form
    if request.method == "GET":
        return render_template('new.html')

    # create an idea 
    # redirect to author's ideas
    else:
        if request.form['title'] == '' or request.form['content'] == '':
            return render_template('new.html', error='at least try to write something')

        user = users.get_current_user()
        return redirect('/' + str(user.nickname()))

def full_view(idea_id):
    """Full idea"""
    return render_template('full.html')

def author(author):
    """List of author's ideas"""
    return render_template('ideas_list.html', author=author)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500
