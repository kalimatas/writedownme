from functools import wraps
from hashlib import md5
from flask import render_template
from flask import request
from flask import redirect
from flask import abort
from application import app

from google.appengine.api import users
from google.appengine.ext import db
from application import models

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

    query = models.Idea.all()
    query.order("-date")
    ideas = query.fetch(20)

    return render_template("ideas_list.html", ideas=ideas, logout_url=users.create_logout_url("/"))

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

        author = users.get_current_user()

        title = request.form['title']
        content = request.form['content']
        author_id = author.user_id()
        author_nickname = author.nickname()
        idea = models.Idea(title=title, content=content, author_id=author_id, author_nickname=author_nickname)

        try:
            idea.put() 
        except Exception:
            return abort(500)

        return redirect('/' + str(users.get_current_user().nickname()))

def full_view(idea_id):
    """Full idea"""
    return render_template('full.html')

def author(author):
    """List of author's ideas"""

    query = models.Idea.all()
    query.filter("author_nickname", author)
    query.order("-date")
    ideas = query.fetch(20)

    return render_template('ideas_list.html', author=author, ideas=ideas)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

