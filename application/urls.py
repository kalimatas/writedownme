from application import app
from application import views

app.add_url_rule('/', view_func=views.latest_ideas)
app.add_url_rule('/new', view_func=views.add_new_idea, methods=['GET', 'POST'])
app.add_url_rule('/idea/<int:idea_id>', view_func=views.full_view)
