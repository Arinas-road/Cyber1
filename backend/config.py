# will contain main configuration of our app

# [1] we build the api first, which happens in Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# CORS stands for Cross Origin Requests
# CORS allows as to to send a request to this backend from a different URL
# be default, when we send requests, our server will be protected, so it can't be hit from a different URL
# In our case, our frontend is a different server than the backend and we want to be able to communicate, so we remove this CORS error, which can pop up

app = Flask(__name__)
CORS(app) #disables the error described above

# [2] initializing database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
#here we are specifying the location of the local SQL lite database (storing a file)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # disabling tracking modifications we make to a database, to make life easier

db = SQLAlchemy(app) # creates database instance, which gives us access to the database that we specified in line 16
