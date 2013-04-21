import os

from flask import render_template, make_response
from views.render_template import RenderTemplateView

class DownloadView(RenderTemplateView):
	def __init__(self, *args, **kwargs):
		super(DownloadView, self).__init__(*args, **kwargs)

	def dispatch_request(self):
		from run import app
		files = os.listdir(app.config['UPLOAD_FOLDER'])
		return render_template('download.html', files = files)
