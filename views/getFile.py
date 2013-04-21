import os

from flask import request, send_file
from views.render_template import RenderTemplateView

class getFileView(RenderTemplateView):
	def __init__(self, *args, **kwargs):
		super(getFileView, self).__init__(*args, **kwargs)
	
	def dispatch_request(self):
		#here's the problem:
		self.index = request.args.get('index')
		from run import app
		files = os.listdir(app.config['UPLOAD_FOLDER'])
		fullpath = app.config['UPLOAD_FOLDER'] + "/" + files[int(self.index)]
		return send_file(fullpath, as_attachment=True)
