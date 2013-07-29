# Docs http://flask.pocoo.org/docs/views/ on this structure type.
# Configure View URLs.
from syncomatic import views
from syncomatic import app

app.add_url_rule('/', view_func=views.RootView.as_view('index',\
    template_name='index.html'))

app.add_url_rule('/getFile', view_func=views.getFileView.as_view('getFile'))

app.add_url_rule('/deleteFile', view_func=views.deleteFileView.as_view('deleteFile'))

app.add_url_rule('/login', view_func=views.LoginView.as_view('login',\
    template_name='login.html'))

app.add_url_rule('/logout', view_func=views.LogoutView.as_view('logout'))

app.add_url_rule('/register', view_func=views.RegisterView.as_view('register',\
    template_name='register.html'))

app.add_url_rule('/create_folder',
                 view_func=views.CreateFolderView.as_view('create_folder'))

app.add_url_rule('/change_folder',
                 view_func=views.ChangeFolderView.as_view('change_folder'))

app.add_url_rule('/share_file',
                 view_func=views.ShareFileView.as_view('share_file'))

app.add_url_rule('/contact', view_func=views.RenderTemplateView.as_view('contact',\
    template_name='contact.html'))
app.add_url_rule('/about', view_func=views.RenderTemplateView.as_view('about',\
    template_name='about.html'))
