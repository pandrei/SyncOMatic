from flask import Flask, render_template, abort
app = Flask(__name__)

# Docs http://flask.pocoo.org/docs/views/ on this structure type.
# Configure View URLs.
from views import RootView, DownloadView, getFileView
app.add_url_rule('/', view_func=RootView.as_view('index',\
    template_name='index.html'))
app.add_url_rule('/download', view_func=DownloadView.as_view('dowload',\
    template_name='download.html'))
app.add_url_rule('/getFile', view_func=getFileView.as_view('getFile',\
    template_name='download.html'))

# The folder where files will be uploaded.
import os
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'files')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == '__main__':
    app.run(debug=True)
