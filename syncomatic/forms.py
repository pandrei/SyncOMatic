import os
import shutil, errno

from flask.ext.wtf import Form, BooleanField, PasswordField, Required
from flask.ext.wtf.html5 import EmailField
from flask.ext.wtf.file import FileField

from wtforms.validators import ValidationError, equal_to
from wtforms.fields import HiddenField
from werkzeug import secure_filename

from syncomatic.models import User

class LoginForm(Form):
    email = EmailField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

    def validate_email(form, field):
        """The user should exist if one wants to login with him."""
        if not User.query.filter_by(email = field.data).first():
            raise ValidationError("Email is incorrect.")

    def validate_password(form, field):
        """The user should exist if one wants to login with him."""
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            if not user.has_password(field.data):
                raise ValidationError("Password is incorrect.")

class RegisterForm(Form):
    email = EmailField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required(),
                             equal_to('confirm_password')])
    confirm_password = PasswordField('confirm_password',
                                     validators = [Required()])

    def validate_email(form, field):
        """Check if the registered user already exists and raise err."""
        if User.query.filter_by(email = field.data).first():
            raise ValidationError("Email already registed.")

    def register_user(self):
        """Register a given user."""
        User.add_user(User(self.email.data, self.password.data))

class UploadForm(Form):
    """Form used for uploading files. This form
       is intended only for validation purposes.
    """
    upload = FileField("Upload your image", validators=[Required()])

    def save_file(self, path):
        filename = secure_filename(self.upload.data.filename)
        self.upload.data.save(os.path.join(path, filename))

class CreateFolderForm(Form):
    """Form used for uploading files. This form
       is intended only for validation purposes.
    """
    directory = HiddenField("The new directory", validators=[Required()])

    def create_directory(self, current_path):
        new_dir = os.path.join(current_path, self.directory.data)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

def copytree(src, dst, symlinks=False, ignore=None):
    # The source is a directory, copy it recursively.
    if os.path.isdir(src):
        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                copytree(s, d, symlinks, ignore)
            else:
                if not os.path.exists(d) or os.stat(src).st_mtime - os.stat(dst).st_mtime > 1:
                    shutil.copy2(s, d)
    # Source is a file, simple copy.
    else:
        shutil.copy2(src, dst)

class ShareFileForm(Form):
    """Form used for sharing files. This form
       is intended only for validation purposes.
    """
    path = HiddenField("The share email", validators=[Required()])
    index = HiddenField("The share email", validators=[Required()])
    email = HiddenField("The share email", validators=[Required()])

    def share_directory(self):
        """Actually copy recursively a file/folder into another
           user's home path.
        """
        # Get the user to share file/folder with.
        share_user = User.query.filter_by(email = self.email.data).first()
        if not share_user:
            return

        # The source to copy to another user.
        filename = os.listdir(self.path.data)[int(self.index.data)]
        src = os.path.join(self.path.data, filename)
        # Get home path for the user to share folder with.
        dst = os.path.join(share_user.get_files_path(), filename)
        # Copy source to destination.
        copytree(src, dst)
