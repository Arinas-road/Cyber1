import logging
import secrets
import base64
import random
import socket
import json
from flask import request, jsonify
from datetime import datetime

from config import app, db
from models import Contact, EncryptionKey, Task, User
from base64 import b64decode
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Settings
PORT: int = 12345
BUFFER_SIZE: int = 1024
FORMAT: str = 'utf-8'
DISCONNECT_MSG: str = "DISCONNECT"
LENGTH_FIELD_SIZE: int = 2
HEADER_SIZE: int = 4
ARG_SEPARATOR = '<'
COMMAND_SEPARATOR = '>'
NUM_OF_COPY_ARGS = 2
COMMAND_INDEX = 0
ARG_INDEX = 1
SOURCE_INDEX = 0
DEST_INDEX = 1

#__________________________________________________________________________________
# Helping functions
LOG_FILE = 'LOG.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def write_to_log(msg):
    logging.info(msg)
    print(msg)
    

def generate_random_key(key_length=32):
  """
  Generates a cryptographically secure random key.
  Args: key_length: The desired length of the key in bytes.
  Returns: The generated key as a base64-encoded string.
  """
  random_bytes = secrets.token_bytes(key_length)
  byte_string = base64.b64encode(random_bytes)
  return byte_string.decode('utf-8')

def generate_random_iv():
    byte_string =  "".join(str(random.randint(0, 9)) for _ in range(16))
    return byte_string


#__________________________________________________________________________________
# Encryption
def set_encryption():
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
        # else:
        #     existing_key[0].iv = generate_random_iv()
        #     db.session.commit()

#Get EncryptionKey
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

# Decryption
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

#Get Users - returns list of users
def get_contacts():
    users = User.query.all() #gets all different contexts that exist inside the Contact
    json_users = list(map(lambda x: x.to_json(), users))
    
    return jsonify({"contacts": json_users})

#Add New User
def create_contact(data):
    # looking for data that was submitted
    # use get, cause if the value doesnt exist it will return None
    if not data:
        return jsonify({"message": "Something is wrong with the user data!"}), 400 # response + error code
    # if above wasnt the case, then we need to create a new contact, add in db and say that everything is fine
    # create python class
    # current_dateTime = 
    
    new_user = User(secretCode=data["secretCode"],
                       username=data["username"],
                       firstName=data["firstName"], 
                       lastName=data["lastName"], 
                       birthDate=data["birthDate"], 
                       email=data["email"],
                       profilePicture=data["profilePicture"],
                       rights=data["rights"],
                       isLoggedIn=data["isLoggedIn"],
                       createdAt=datetime.now(),
                       updatedAt=datetime.now(),
                       helping_requests=data["helping_requests"],
                       className=data["className"],
                       #User speciic - Teacher
                       gradesTeaching=data["gradesTeaching"],
                       subjectsTeaching=data["subjectsTeaching"],
                       #User speciic - Student
                       StudyingInGrade=data["StudyingInGrade"],
                       specialSkills=data["specialSkills"],
                       #User specific - Administartion
                       )
    
    #try to add to db
    try:
        db.session.add(new_user)
        db.session.commit() # writes in db permanently
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "User created!!!"}), 201 

#UPDATE EXISTING USER
def update_contact(user_id, data):
    user = User.query.get(user_id)
    
    # if no user with that id exists
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    
    #if we did find the contact
    write_to_log(f"[main.py][update_contact] - contact from user:{data} ")
    username = data.get("username", user.username)
    firstName = data.get("firstName", user.firstName)
    lastName = data.get("lastName", user.lastName)
    birthDate = data.get("birthDate", user.birthDate)
    email = data.get("email", user.email)
    profilePicture = data.get("profilePicture", user.profilePicture)
    helping_requests = data.get("helping_requests", user.helping_requests)
    className = user.className
    #User speciic - Teacher
    gradesTeaching = data.get("gradesTeaching", user.gradesTeaching)
    subjectsTeaching = data.get("subjectsTeaching", user.subjectsTeaching)
    #User speciic - Student
    StudyingInGrade = data.get("StudyingInGrade", user.StudyingInGrade)
    specialSkills = data.get("specialSkills", user.specialSkills)   
    
    #Change it later!!!!:
    
    decrypted_username = decrypt_text(username)
    write_to_log(f"[main.py][update_contact] username decryprted: {decrypted_username}")
    decrypted_first_name = decrypt_text(firstName)
    write_to_log(f"[main.py][update_contact] firstName decryprted: {decrypted_first_name}")
    decrypted_last_name = decrypt_text(lastName)
    write_to_log(f"[main.py][update_contact] laststName decryprted: {decrypted_last_name}")
    decrypted_birth_date = decrypt_text(birthDate)
    write_to_log(f"[main.py][update_contact] birthDate decryprted: {decrypted_birth_date}")
    decrypted_email = decrypt_text(email)
    write_to_log(f"[main.py][update_contact] email decryprted: {decrypted_email}")
    decrypted_profile_picture = decrypt_text(profilePicture)
    write_to_log(f"[main.py][update_contact] profile picture decryprted: {decrypted_profile_picture}")
    # decrypted_rights = decrypt_text(rights)
    # write_to_log(f"[main.py][update_contact] rights decryprted: {decrypted_rights}")
    #decrypted_is_loggen_in = decrypt_text(isLoggedIn)
    #write_to_log(f"[main.py][update_contact] isLoggedIn decryprted: {decrypted_is_loggen_in}")
    #decrypted_created_at = decrypt_text(createdAt)
    #write_to_log(f"[main.py][update_contact] createdAt decryprted: {decrypted_created_at}")
    #decrypted_updated_at = decrypt_text(updatedAt)
    #write_to_log(f"[main.py][update_contact] updatedAt decryprted: {decrypted_updated_at}")
    decrypted_helping_requests = decrypt_text(helping_requests)
    write_to_log(f"[main.py][update_contact] helping requests decryprted: {decrypted_helping_requests}")
    decrypted_class_name = decrypt_text(className)
    write_to_log(f"[main.py][update_contact] className decryprted: {decrypted_class_name}")

    user.username = decrypted_username
    user.firstName = decrypted_first_name
    user.lastName = decrypted_last_name
    user.birthDate = decrypted_birth_date
    user.email = decrypted_email
    user.profilePicture = decrypted_profile_picture
    user.helping_requests = decrypted_helping_requests
    user.className = decrypted_class_name
    current_dateTime = datetime.now()
    user.updatedAt = current_dateTime
    #User specific 
    if user.className == "Teacher":
        decrypted_grades_teaching = decrypt_text(gradesTeaching)
        write_to_log(f"[main.py][update_contact] gradesTeaching decryprted: {decrypted_grades_teaching}")
        decrypted_subjects_teaching = decrypt_text(subjectsTeaching)
        write_to_log(f"[main.py][update_contact] subjectsTeaching decryprted: {decrypted_subjects_teaching}")
        user.gradesTeaching = decrypted_grades_teaching
        user.subjectsTeaching = decrypted_subjects_teaching
    if user.className == "Student":
        decrypted_studying_in_grade = decrypt_text(StudyingInGrade)
        write_to_log(f"[main.py][update_contact] StudyingInGrade decryprted: {decrypted_studying_in_grade}")
        decrypted_special_skills = decrypt_text(specialSkills)
        write_to_log(f"[main.py][update_contact] specialSkills decryprted: {decrypted_special_skills}")
        user.StudyingInGrade = decrypted_studying_in_grade
        user.specialSkills = decrypted_special_skills
    if user.className == "Administration":
        pass
    #after we've modified, we want to save
    db.session.commit()
    
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return jsonify({"message": "User updated!!!"}), 200

#DELETE EXISTING USER
def delete_contact(user_id):
    contact = Contact.query.get(user_id)
    
    # if no user with that id exists
    if not contact:
        return jsonify({"message": "User not found"}), 404
    
    #deleting
    db.session.delete(contact)
    db.session.commit()
    
    return jsonify({"message": "User deleted!!!"}), 200

#__________________________________________________________________________________
# Client-Server Communication

Cmd_array = ["ADD_USER", "DELETE_USER", "UPDATE_USER", "GET_USERS", "GET_KEY"]

def receive_msg(my_socket: socket) -> (bool, str):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    str_header = my_socket.recv(1024)
    write_to_log(f"[protocol.py] [receive_msg] str_header received: {str_header}")
    # length = int(str_header)
    # if length > 0:
    #     buf = my_socket.recv(length).decode(FORMAT)
    # else:
    #     return False, ''

    # return True, buf
    return 'a'

def check_cmd(data) -> bool:
    # write to log
    write_to_log("[PROTOCOL] - CHECK_CMD - data is " + data)
    # we check if the command entered by user aligns with our list of commands
    """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""
    if data in Cmd_array:
        # if it is one of our values we return true
        write_to_log("[PROTOCOL] data is correct")
        return True
    else:
        # if it is not one of our values we return false
        return False

def create_request_msg(cmd: str, args: str = "") -> str:
    """Create a valid protocol message, will be sent by client, with length field"""
    # we add before msg itself its length, so we can tell how much space the message is going to take
    request = ""
    if check_cmd(cmd):
        # create string that looks like cmd>args
        request = cmd + ">" + "<".join(args)
        if cmd == "REG":
            json_args = json.loads(args)
            request = cmd + ">" + "<".join(json_args)
        # write to log
        write_to_log("[PROTOCOL - CRT-MSG] request - " + request)
        # return string with header with length 4 and request itself
        return f"{len(request):04d}{request}"
    else:
        request = "Command is not supported by this version of protocol"
        # write to log
        write_to_log("[PROTOCOL - CRT-MSG] request is not supported- " + request)

        return f"{len(request):04d}{request}"
    
def create_response_msg(cmd: str, args = '') -> str:
    # creates response msg according to what command user sent
    """Create a valid protocol message, will be sent by server, with length field"""
    response = "Non-supported cmd"
    # write to log
    write_to_log("[PROTOCOL] creates response msg with -" + cmd)
    # check cmd name and executes a function
    if cmd == "ADD_USER":
        response = create_contact(args)
    elif cmd == "DELETE_USER":
        response = delete_contact(args)  
    elif cmd == "UPDATE_USER":
        response = update_contact(args)  
    elif cmd == "GET_USERS":
        response = get_contacts()
    elif cmd == "GET_KEY":
        response = get_encryption_key() 
    elif cmd == DISCONNECT_MSG:
        response = DISCONNECT_MSG
    return f"{len(response):04d}{response}"

def parse_buffer(request) -> (str, str):
    """
    parse the request and return a tuple of the command and argument
    :param request: the request received from the client
    :return: a tuple with the command and argument
    """
    split_request = request.split(COMMAND_SEPARATOR)
    command = split_request[COMMAND_INDEX]
    arg = ''
    if len(split_request) == ARG_INDEX + 1:
        arg = split_request[ARG_INDEX]
    return command, arg


def parse_request(buf: str) -> str:
    # split buf for parts before and after >
    split_request = buf.split('>')
    # get the first part (cmd) before > in buf
    cmd = split_request[0]
    # get the second part (args) after > in buf
    args = split_request[1][2:len(split_request[1]) - 2]
    return cmd, args