from flask.views import View

class RootView(View):

    def dispatch_request(self):
        return "Hello"
