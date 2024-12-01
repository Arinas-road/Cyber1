# we need an operation for Creating, Reading/Getting, Updating and Deleting

# Create (in order to create a contact we need:)
# - first name
# - last name
# - email

#localhost:5000/get_contact (after / - endpoint)

# Request (fr -> bck)
# type: DELETE
# json: we'll need to pu a type of contact we want to delete

# Response (bck -> fr)
# status: 200 (successfull or not)
# json: {info we return}

from flask import request, jsonify
from config import app, db
from models import Contact

# GET
# decorator, create route "/contacts", specify valid methods for certain URL 
@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all() #gets all different contexts that exist inside the Contact
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    
    return jsonify({"contacts": json_contacts})
    
#CREATE
# writing route for creating contacts
@app.route("/create_contact", methods=["POST"])
def create_contact():
    # looking for data that was submitted
    # use get, cause if the value doesnt exist it will return None
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")
    
    if not first_name or not last_name or not email:
        return jsonify({"message": "You must include a first name, last name and email"}), 400 # response + error code

    # if above wasnt the case, then we need to create a new contact, add in db and say that everything is fine
    # create python class
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    
    #try to add to db
    try:
        db.session.add(new_contact)
        db.session.commit() # writes in db permanently
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "User created!!!"}), 201 

#UPDATE
#<update exact user id> like <"/update_contact/1">
@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)
    
    # if no user with that id exists
    if not contact:
        return jsonify({"message": "User not found"}), 404
    
    #if we did find the contact
    data = request.json
    # if you gave a new first name, we are going to change it, otherwise it will stay the same
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)
    
    #after we've modified, we want to save
    db.session.commit()
    
    return jsonify({"message": "User updated!!!"}), 200

#DELETE
@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])

def delete_contact(user_id):
    contact = Contact.query.get(user_id)
    
    # if no user with that id exists
    if not contact:
        return jsonify({"message": "User not found"}), 404
    
    #deleting
    db.session.delete(contact)
    db.session.commit()
    
    return jsonify({"message": "User deleted!!!"}), 200


# run flask application:
if __name__ == "__main__": #if you actually ran main.py, then execute code
    with app.app_context():
        db.create_all() # if it doesnt exist, creates all different models that we have defined in db
    
    app.run(debug=True)
