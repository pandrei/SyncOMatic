from flask import Flask, render_template, abort
app = Flask(__name__)

# Docs http://flask.pocoo.org/docs/views/ on this structure type.
# Configure View URLs.
from views import RootView
app.add_url_rule('/', view_func=RootView.as_view('home_view'))

if __name__ == '__main__':
    app.run(debug=True)
