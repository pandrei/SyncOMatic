import os
import shutil
import zipfile

from flask import render_template, redirect, url_for, request, g, send_file
from flask.ext.login import login_user, current_user, logout_user
from flask.views import View

from syncomatic import app, lm
from syncomatic.decorators import login_required
from syncomatic.forms import (LoginForm, RegisterForm, UploadForm,
                              CreateFolderForm, ShareFileForm)
from syncomatic.models import User
from syncomatic import foos

class RenderTemplateView(View):
    """
        This views's purpose is to render a given template.
        Extend it at your own will.
    """
    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self, *args, **kwargs):
        return render_template(self.template_name, **kwargs)


@lm.user_loader
def load_user(id):
    """Has the purpose of telling flask-login what to use
       to load a user from database. Hence the decorator.
    """
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


class RootView(RenderTemplateView):
    """
        This view manages the index page, and displays all the
        uploaded files by a user and also it provides a form
        for uploading new files.
    """
    methods = ['GET', 'POST']

    def dispatch_request(self):
        form = UploadForm()

        # Render the template now if the user is not authenticateed.
        if not g.user.is_authenticated():
            return super(RootView, self).dispatch_request(self)

        # Get the user directory.
        base_path = g.user.get_files_path()
        path_message = '/'
        if request.args.get('path'):
            current_path = request.args.get('path')
            # If current path is not '/' we update the location message
            if not current_path == base_path:
                path_message = current_path[len(base_path):]
        else:
            current_path = base_path

        # If we've got a GET request, just render the template with
        # all the uploaded files by the user.
        if request.method == 'GET':
            files = foos.get_filelist(current_path)
            # Return just the relative path to the base path
            return super(RootView, self).dispatch_request\
                (path=current_path, path_msg=path_message,
                 files=files, user=g.user, form=form)
        # A file upload was done.
        elif request.method == 'POST':
            if form.validate_on_submit():
                form.save_file(current_path)
                return redirect(url_for('index', path=current_path))
            files = foos.get_filelist(current_path)
            # Re-render the index page with upload information regarding the
            # uploaded file through POST.
            return super(RootView, self).dispatch_request\
                (path=current_path, path_msg=path_message,
                 files=files, user=g.user,
                 form=form)


class getFileView(View):
    """
        This view's purpose is to allow a user to download files, thus it does
        not need a template associated with it.
    """
    def get_filepath_by_index(self, path, index):
        # Get the user directory.
        if path:
            current_path = path
        else:
            current_path = g.user.get_files_path()
        # Get the file index that is wanted to be downloaded.
        files = os.listdir(current_path)
        # Target the file one wants to download and send it.
        fullpath = os.path.join(current_path, files[int(index)])
        return fullpath

    def dispatch_request(self):
        index = request.args.get('index')
        fullpath = self.get_filepath_by_index(request.args.get('path'), index)
        if os.path.isfile(fullpath):
            return send_file(fullpath, as_attachment=True)
        else:
            # TODO function that returns the zip folder path using g.user.get()
            zipfolder = g.user.get_files_path() + 'zips'
            if not os.path.exists(zipfolder):
                os.makedirs(zipfolder)
            zipname = foos.get_unused_name(zipfolder)

            zip = zipfile.ZipFile(os.path.join(zipfolder, zipname), 'w')
            foos.zipdir(fullpath, zip)
            zip.close()
            
            return send_file(os.path.join(zipfolder, zipname), as_attachment=True)


class deleteFileView(getFileView):
    """
        This view's purpose is to allow a user to delete a file, thus it does
        not need a template associated with it.
    """
    def dispatch_request(self):
        current_path = request.args.get('path')
        index = request.args.get('index')
        # Target the file one wants to delete
        fullpath = self.get_filepath_by_index(current_path, index)
        if os.path.exists(fullpath):
            if os.path.isfile(fullpath):
                os.unlink(fullpath)
            else:
                shutil.rmtree(fullpath)
        # Re-render root page (/)
        return redirect(url_for('index', path=current_path))


class LoginView(RenderTemplateView):
    methods = ['GET', 'POST']

    def __init__(self, *args, **kwargs):
        super(LoginView, self).__init__(*args, **kwargs)

    def dispatch_request(self):
        # User has logged in successfully before.
        if g.user is not None and g.user.is_authenticated():
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            # If user exists in our DB, log him in.
            if user:
                login_user(user, remember = form.remember_me.data)
                # Delete old user zip folder
                zipfolder = g.user.get_files_path() + 'zips'
                if os.path.exists(zipfolder):
                    shutil.rmtree(zipfolder)
                return redirect(url_for('index'))
            return redirect(url_for('login'))
        return super(LoginView, self).dispatch_request(title='Sign In',
                                                       form=form)

class RegisterView(RenderTemplateView):
    methods = ['GET', 'POST']

    def __init__(self, *args, **kwargs):
        super(RegisterView, self).__init__(*args, **kwargs)

    def dispatch_request(self):
        # User has logged in successfully before.
        if g.user is not None and g.user.is_authenticated():
            return redirect(url_for('index'))
        form = RegisterForm()
        if form.validate_on_submit():
            form.register_user()
            # Now redirect the user to login so he may login.
            return redirect(url_for('login'))
        return super(RegisterView, self).dispatch_request(title='Register',
                                                          form=form)


class LogoutView(View):
    methods = ['GET']

    def dispatch_request(self):
        logout_user()
        return redirect(url_for('index'))

class CreateFolderView(View):
    methods = ['POST']

    @login_required
    def dispatch_request(self):
        # url_for in template send extra argument current_path
        current_path = request.args.get('path')
        form = CreateFolderForm(request.form)
        if form.validate_on_submit():
            form.create_directory(current_path)
        # We pass current_path further, we need to keep track of our position
        return redirect(url_for('index', path=current_path))

class ChangeFolderView(getFileView):
    methods = ['GET']

    @login_required
    def dispatch_request(self):
        # url_for in template send extra argument current_path
        current_path = request.args.get('path')
        index = request.args.get('index')
        if index == str(-1):
            new_path = os.path.dirname(current_path)
        else:
            new_path = self.get_filepath_by_index(current_path, index)
        return redirect(url_for('index', path=new_path))

class ShareFileView(getFileView):
    methods = ['POST']

    @login_required
    def dispatch_request(self):
        # url_for in template send extra argument current_path
        form = ShareFileForm(request.form)
        current_path = form.path.data
        if form.validate_on_submit():
            form.share_directory()
        return redirect(url_for('index', path=current_path))
