from application import app
from application import views

app.add_url_rule('/', view_func=views.latest_ideas)
app.add_url_rule('/page/<int:page>', view_func=views.latest_ideas)
app.add_url_rule('/new', view_func=views.add_new_idea, methods=['GET', 'POST'])
app.add_url_rule('/idea/<int:idea_id>', view_func=views.full_view)
app.add_url_rule('/<author>', defaults={'page': 0}, view_func=views.author)
app.add_url_rule('/<author>/page/<int:page>', view_func=views.author)
