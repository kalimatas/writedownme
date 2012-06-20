from functools import wraps
from hashlib import sha256
from textile import textile
from flask import render_template
from flask import request
from flask import redirect
from flask import abort
from application import app

from google.appengine.api import users
from google.appengine.ext import db
from application import models

IDEAS_PER_PAGE = 20
SALT = 'idea_project_salt'

def auth_required(aFunc):
    """Require login"""
    @wraps(aFunc)
    def _auth_wrapper(*args, **kwargs):
        if not users.get_current_user():
            return redirect(users.create_login_url(request.url))
        return aFunc(*args, **kwargs)
    return _auth_wrapper

def latest_ideas(page=0):
    """List of latest ideas"""

    query = models.Idea.all()
    query.order("-date")
    ideas_count = query.count()
    ideas = query.fetch(IDEAS_PER_PAGE, page * IDEAS_PER_PAGE)

    has_next = ideas_count > (page * IDEAS_PER_PAGE + IDEAS_PER_PAGE)
    current_user = users.get_current_user()

    return render_template("ideas_list.html", 
                           ideas=ideas, 
                           logout_url=users.create_logout_url("/"),
                           current_page=page,
                           current_user=current_user,
                           has_next=has_next)

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
        content = textile(request.form['content'])
        author_id = author.user_id()
        author_nickname = author.nickname()
        hash = sha256(SALT + author.nickname() + title).hexdigest()
        idea = models.Idea(title=title, content=content, author_id=author_id, author_nickname=author_nickname, hash=hash)

        try:
            idea.put() 
        except Exception:
            return abort(500)

        return redirect('/' + str(users.get_current_user().nickname()))

@auth_required
def delete_idea(hash):
    back_url = '/' if request.referrer is None else request.referrer
    return redirect(back_url)

@auth_required
def edit_idea(hash):
    pass

def full_view(idea_id):
    """Full idea"""
    idea = models.Idea.get_by_id(idea_id)
    if not idea:
        return abort(404)

    return render_template('full.html', idea=idea)

def author(author, page=0):
    """List of author's ideas"""

    query = models.Idea.all()
    query.filter("author_nickname", author)
    query.order("-date")
    ideas_count = query.count()
    ideas = query.fetch(IDEAS_PER_PAGE, page * IDEAS_PER_PAGE)

    has_next = ideas_count > (page * IDEAS_PER_PAGE + IDEAS_PER_PAGE)
    current_user = users.get_current_user()

    return render_template('ideas_list.html', 
                           author=author, 
                           ideas=ideas,
                           current_page=page,
                           current_user=current_user,
                           has_next=has_next)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

