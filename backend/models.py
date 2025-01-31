# will contain all our database models
# Flask-SQLAlchemy - we create a python class, which represents a row in our database
# And we define the different columns and data that this object will be storing

from config import db

# this is going to be a database model represented as a Python class
# And now in python code we can define different fields that this object will have
class Contact(db.Model): 
    __tablename__ = "Contacts"
    # (type of a field, unique key)
    id = db.Column(db.Integer, primary_key = True)
    # db.String(maximum length in characters), nullable False - you can't leave it empty, unique - no two contacts can have the same value
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
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
    
# need to add creator's name???
class Task(db.Model):
    __bind_key__ = "Task"
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    date = db.Column(db.String(80), unique=False, nullable=False)
    time = db.Column(db.String(80), unique=False, nullable=False)
    location = db.Column(db.String(80), unique=False, nullable=False)
    numPeople = db.Column(db.Integer, unique=False, nullable=False)
    optionalInfo = db.Column(db.String(120), unique=False, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date,
            "time": self.time,
            "location": self.location,
            "numPeople": self.numPeople,
            "optionalInfo": self.optionalInfo,
        }
        
class EncryptionKey(db.Model):
    __bind_key__ = "EncryptionKey"  # Only needed if you are using multiple databases
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(256), unique=True, nullable=True)  # Store the key as binary data
    iv = db.Column(db.String(), unique=True, nullable=True)
    def to_json(self):
        return {
            "id": self.id,
            "key": self.key,  # Encode binary key to Base64 before returning as JSON
            "iv": self.iv,
        }


class User(db.Model):
    __bind_key__= "User"
    id = db.Column(db.Integer, primary_key = True)
    secretCode = db.Column(db.String(), unique=True, nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    firstName = db.Column(db.String(), unique=False, nullable=False)
    lastName = db.Column(db.String(), unique=False, nullable=False)
    birthDate = db.Column(db.String(), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profilePicture = db.Column(db.String(), unique=True, nullable=True) #What type of data?!
    rights = db.Column(db.String(), unique=False, nullable=False)
    isLoggedIn = db.Column(db.String(), unique=False, nullable=False)
    createdAt = db.Column(db.String(), unique=False, nullable=False)
    updatedAt = db.Column(db.String(), unique=False, nullable=False)
    helping_requests = db.Column(db.String(), unique=False, nullable=False) #creat class Helpng Request consisting of Tasks!!!
    className = db.Column(db.String(), unique=False, nullable=False)
    #User speciic - Teacher
    gradesTeaching = db.Column(db.String(), unique=False, nullable=True)
    subjectsTeaching = db.Column(db.String(), unique=False, nullable=True)
    #User speciic - Student
    StudyingInGrade = db.Column(db.String(), unique=False, nullable=True)
    specialSkills = db.Column(db.String(), unique=False, nullable=True)
    #User specific - Administartion
    
    def to_json(self):
        return{
            "id": self.id,
            "secretCode": self.secretCode,
            "username": self.username,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "birthDate": self.birthDate,
            "email": self.email,
            "profilePicture": self.profilePicture,
            "rights": self.rights,
            "isLoggedIn": self.isLoggedIn,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
            "helping_requests": self.helping_requests,
            #User speciic - Teacher
            "gradesTeaching": self.gradesTeaching,
            "subjectsTeaching": self.subjectsTeaching,
            #User speciic - Student
            "StudyingInGrade": self.StudyingInGrade,
            "specialSkills": self.specialSkills,
            #User specific - Administartion
        }
        
