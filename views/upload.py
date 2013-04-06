import os

from flask import request, url_for, redirect
from flask.views import View
from werkzeug import secure_filename

class UploadView(View):
    methods = ['POST']

    def __init__(self):
        self.allowed_extensions =\
            set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in self.allowed_extensions

    def dispatch_request(self):
        from run import app
        file = request.files['file']
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
