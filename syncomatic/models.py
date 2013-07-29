import os
import hashlib

from flask.ext.sqlalchemy import SQLAlchemy
from syncomatic import app

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(64))

    def __init__(self, email, password):
        self.email = email
        # Store a hash of the password.
        self.password = User.get_hexdigest(password)

    def __repr__(self):
        return '<User %r>' % self.email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def has_password(self, password):
        """Check if a given password is the same as the stored hash."""
        return User.get_hexdigest(password) == self.password

    def get_files_path(self):
        """Get the path where the user's files are stored.
           The user directory looks like this:
                files/$id/
           where the $id is the self.id of the user who requests the files.
        """
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(self.id))
        # Create the user directory if it does
        # not already exist.
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    @staticmethod
    def get_hexdigest(password):
        return hashlib.sha1(password).hexdigest()

    @staticmethod
    def add_user(user):
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def initdb():
        """Delete old database, init a new one and populate it.
           We do this to sync changes on the models, when runnig
           run.py.

           Order is important. This has to be called only after the User
           model has been defined.
        """
        if os.path.exists(app.config['SQLALCHEMY_DATABASE_URI_PATH']):
            os.unlink(app.config['SQLALCHEMY_DATABASE_URI_PATH'])
        db.create_all()
        User.add_user(User('admin@example.com', 'admin'))
