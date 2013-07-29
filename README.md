SyncOMatic
==========

##How to run:

* install flask, follow [docs guide](http://flask.pocoo.org/docs/installation/#installation)
* install all needed packets from `requirements.txt` file, all using `pip install $name`
* `$ ./run.py` opens server listening on [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
* `$ ./run.py --initdb` does the same thing but it also creates the database,
  for the times when you want to erase your database. The default user added into
  database is **admin@example.com** with password **admin**.
* **NOTE**: you should run with `--initdb` first time, when you don't have a
  database created.


##What it can do (in progress):

* upload a file using the file chooser, and store it in **project/files/**
* download a file (to local) that was uploaded
* download a folder by archive, it zips the folder content
* create folders
* access folders and their parent-folder
* delete files and folders
* login and logout with a user in the app, it doesn't take into account the password for now and
  no registrations possible for now, just hardcoded account created in the database
  * database is in `syncomatic/static/syncomatic.db`
