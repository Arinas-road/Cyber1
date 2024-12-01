# will contain all our database models
# Flask-SQLAlchemy - we create a python class, which represents a row in our database
# And we define the different columns and data that this object will be storing

from config import db

# this is going to be a database model represented as a Python class
# And now in python code we can define different fields that this object will have
class Contact(db.Model): 
    # (type of a field, unique key)
    id = db.Column(db.Integer, primary_key = True)
    # db.String(maximum length in characters), nullable False - you can't leave it empty, unique - no two contacts can have the same value
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # will take all our fields on our object and convert it into a python dictionary, which we can then convert into JSON
    # and JSON we can pass from our API
    # (when we build an API we communicate via JSON - js object, so we return json and send json)
    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
        }
    