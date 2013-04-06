from flask import render_template
from flask.views import View

class RenderTemplateView(View):
    """
        This views's purpose is to render a given template.
        Extend it at your own will.
    """

    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self, *args, **kwargs):
        return render_template(self.template_name, **kwargs)
