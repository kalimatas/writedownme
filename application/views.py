from flask import render_template
from flask import request
from application import app

def latest_ideas():
    """List ideas of all or chosen author"""
    return render_template('ideas_list.html')

def add_new_idea():
    """Create new idea"""

    # show form
    if request.method == "GET":
        return 'here form'
    # list author's ideas
    else:
        return 'here message'

def full_view(idea_id):
    """Full idea"""
    return render_template('full.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500
