from google.appengine.ext import db
from google.appengine.api import users

class Idea(db.Model):
    """An Idea"""
    author_id = db.StringProperty(required=True)
    author_nickname = db.StringProperty(required=True)
    title = db.StringProperty(required=True)
    content = db.StringProperty(required=True, multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
