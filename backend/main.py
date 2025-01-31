
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

from cryptography.fernet import Fernet
from flask import request, jsonify
from config import app, db
from models import Contact, EncryptionKey, Task, User
import logging
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import secrets
import random
# from dotenv import load_dotenv
# import os

# Take the environment variables from .env file
# load_dotenv()
# FLASK_HOST = os.environment.get("FLASK_HOST")
# FLASK_PORT = os.environment.get("FLASK_PORT")
# WEBPACK_DEV_SERVER_URL = os.environment.get("WEBPACK_DEV_SERVER_URL")

# prepare Log file
LOG_FILE = 'LOG.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def write_to_log(msg):
    logging.info(msg)
    print(msg)
    
#SOCKET
#socket_io = Socket

def generate_random_key(key_length=32):
  """
  Generates a cryptographically secure random key.

  Args:
    key_length: The desired length of the key in bytes.

  Returns:
    The generated key as a base64-encoded string.
  """
  random_bytes = secrets.token_bytes(key_length)
  byte_string = base64.b64encode(random_bytes)
  return byte_string.decode('utf-8')

def generate_random_iv():
    byte_string =  "".join(str(random.randint(0, 9)) for _ in range(16))
    return byte_string


with app.app_context():
        # db.create_all() # if it doesnt exist, creates all different models that we have defined in db
        #ENCRYPTION
        # db.drop_all()
        # db.create_all()
        delete_stmt = db.delete(EncryptionKey) 
        result = db.session.execute(delete_stmt) 
        db.session.commit() 
        existing_key = EncryptionKey.query.all()
        write_to_log(f"[main.py] - Existing keys: {existing_key}")
        if(not existing_key):
            #key_val = "LefjQ2pEXmiy/nNZvEJ43i8hJuaAnzbA1Cbn1hOuAgA="
            
            # Generate a 32-byte (256-bit) key
            encoded_key = str(generate_random_key(32))
            # Print the Base64-encoded AES key
            write_to_log(f"AES Key (Base64 Encoded): {encoded_key}")
            
            iv = generate_random_iv()
            # # Convert the string to bytes (UTF-8 encoded)
            # iv = iv_string.decode('utf-8')
            write_to_log(f"[IV STRING GENERATED] {iv}")
            
            new_key_object = EncryptionKey(key=encoded_key, iv=iv)
            db.session.add(new_key_object)
            db.session.commit()  # Writes to the DB permanently
            write_to_log(f"[main.py] - Created Key: {encoded_key}")
        else:
            existing_key[0].iv = generate_random_iv()
            db.session.commit()
    
def decrypt_text(data: str) -> str:
    # secret_key = "LefjQ2pEXmiy/nNZvEJ43i8hJuaAnzbA1Cbn1hOuAgA="
    key = EncryptionKey.query.all()
    secret_key = key[0].key
    #iv = "1020304050607080"

    iv = key[0].iv
    ciphertext = b64decode(data)
    derived_key = b64decode(secret_key)
    cipher = AES.new(derived_key, AES.MODE_CBC, iv.encode('utf-8'))
    decrypted_data = cipher.decrypt(ciphertext)
    return_value = unpad(decrypted_data, 16).decode("utf-8")
    write_to_log(f"[decryptttt] return value: {return_value}")
    return return_value

#__________________________________________________________________________________
#User


# #DELETE EXISTING USER
# def delete_contact(user_id):
#     contact = Contact.query.get(user_id)
    
#     # if no user with that id exists
#     if not contact:
#         return jsonify({"message": "User not found"}), 404
    
#     #deleting
#     db.session.delete(contact)
#     db.session.commit()
    
#     return jsonify({"message": "User deleted!!!"}), 200


# GET
# decorator, create route "/contacts", specify valid methods for certain URL 
@app.route("/contacts", methods=["GET"])
def get_contacts():
    users = User.query.all() #gets all different contexts that exist inside the Contact
    json_contacts = list(map(lambda x: x.to_json(), users))
    
    return jsonify({"contacts": json_contacts})
@app.route('/get-encryption-key', methods=["GET"])
def get_encryption_key():
    try: 
        key = EncryptionKey.query.all()
        
        encryption_key = key[0].key
        iv = key[0].iv
        write_to_log(f"[GET_ENCRYPTION_KEY] key: {encryption_key}")
        write_to_log(f"[GET_ENCRYPTION_KEY] iv: {iv}")
        
        return jsonify({"key": encryption_key, "iv": iv})
    except Exception as e:
        app.logger.error(f"Error generating key: {e}")
        return jsonify({"error":"Internal Server Error"}), 500

#CREATE
# writing route for creating contacts
@app.route("/create_contact", methods=["POST"])
def create_contact():
    #if we did find the contact
    data = request.json
    write_to_log(f"[main.py][create_contact] - contact from user:{data} ")
    # Create an empty dictionary to store decrypted values
    contact_data = {}
    # Go through the object:
    for key in data:
        value = decrypt_text(data[key])
        contact_data[key] = value  # Store decrypted value
        write_to_log(f"[main.py][create_contact] LOOP {key} decryprted: {value}")
        
    # if above wasnt the case, then we need to create a new contact, add in db and say that everything is fine
   
    
    #try to add to db
    try:
        new_contact = User(**contact_data)  # Unpack dictionary into Contact model
        write_to_log(new_contact)
        db.session.add(new_contact)
        db.session.commit() # writes in db permanently
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "User created!!!"}), 201 

#UPDATE
#<update exact user id> like <"/update_contact/1">
@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = User.query.get(user_id)
    
    # if no user with that id exists
    if not contact:
        return jsonify({"message": "User not found"}), 404
    
    #if we did find the contact
    data = request.json
    write_to_log(f"[main.py][update_contact] - contact from user:{data} ")
    
    # Go through the object:
    for key in data:
        value = decrypt_text(data[key])
        write_to_log(f"[main.py][update_contact] LOOP {key} decryprted: {value}")
        setattr(contact, key, value)  # ✅ Dynamically update the attribute
        write_to_log(f"[main.py][update_contact] LOOP contact.{key}: {getattr(contact, key)}")
    
    # decrypted_first_name = decrypt_text(first_name)
    # write_to_log(f"[main.py][update_contact] firstName decryprted: {decrypted_first_name}")
    # decrypted_first_name = decrypt_text(first_name)
    # write_to_log(f"[main.py][update_contact] firstName decryprted: {decrypted_first_name}")
    # decrypted_last_name = decrypt_text(last_name)
    # write_to_log(f"[main.py][update_contact] firstName decryprted: {decrypted_first_name}")
    # decrypted_first_name = decrypt_text(first_name)
    # write_to_log(f"[main.py][update_contact] firstName decryprted: {decrypted_first_name}")
    # decrypted_email = decrypt_text(email)
    # write_to_log(f"[main.py][update_contact] firstName decryprted: {decrypted_first_name}")

    # contact.first_name = decrypted_first_name
    # contact.last_name = decrypted_last_name
    # contact.email = decrypted_email
    
    #after we've modified, we want to save
    db.session.commit()
    contact = Contact.query.get(user_id)
    # response.headers.add("Access-Control-Allow-Origin", "*")
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
    # db.create_all()
    

    app.run(debug=True)
