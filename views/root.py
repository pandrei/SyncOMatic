import os

from flask import request, url_for, render_template
from werkzeug import secure_filename

from views.render_template import RenderTemplateView

class RootView(RenderTemplateView):
    methods = ['GET', 'POST']

    def __init__(self, *args, **kwargs):
        super(RootView, self).__init__(*args, **kwargs)
        self.allowed_extensions =\
            set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in self.allowed_extensions

    def dispatch_request(self):
        # If we've got a GET request, just render the template.
        if request.method == 'GET':
            return super(RootView, self).dispatch_request()
        # A file upload was done.
        elif request.method == 'POST':
            from run import app
            file = request.files['file']
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                upload_message = 'File %s was successfully uploaded!' % filename
            else:
                upload_message = 'File not provided or not supported format!'
            # Re-render the index page with upload information regarding the
            # uploaded file through POST.
            return render_template('index.html', upload_message=upload_message)
