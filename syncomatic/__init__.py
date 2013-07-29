from flask import Flask
from flask.ext.login import LoginManager

app = Flask(__name__)
# Load config from config.py local file.
app.config.from_object('syncomatic.config')

# The folder where files will be uploaded.
import os

PROJECT_FOLDER = os.path.dirname(os.path.abspath(__file__))

# The folder where files will be uploaded.
app.config['UPLOAD_FOLDER'] = os.path.join(PROJECT_FOLDER, 'files')

# Save the path to the database so we may unlink it and recreate it.
app.config['SQLALCHEMY_DATABASE_URI_PATH'] = os.path.join(PROJECT_FOLDER,
                                                      'static', 'syncomatic.db')
# The database URI that should be used for the connection.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' %\
    app.config['SQLALCHEMY_DATABASE_URI_PATH']

# Create some directories if they don't exist already.
# We need some directories to be created so that our app
# can create the database inside it or to check the uploaded files,
# and git does not allow us to commit empty directories.
DIRS_IN_PROJECT = ['static', 'files']
for d in DIRS_IN_PROJECT:
    # Compute the directory path appending the name to the
    # current path of the project, example
    # /abs/path/application/static/
    d = os.path.join(PROJECT_FOLDER, d)
    if not os.path.exists(d):
        os.makedirs(d)

# Create a login manager, which we'll use for login and storing sessions.
lm = LoginManager()
lm.setup_app(app)

import urls
import models
