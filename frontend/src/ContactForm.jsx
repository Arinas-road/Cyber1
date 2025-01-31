import fernet from 'fernet-web';
//import crypto from 'crypto-js';
import {Encryption, GetKey} from './ClientProtocol.js'
import {useState} from "react"
import CryptoJS from 'crypto-js';
import ClassUser from './Users/ClassUser';

// Add input verification

const ContactForm = ({existingContact={}, updateCallBackContact}) => {
    const [username, setUsername] = useState(existingContact.username || "");
    const [firstName, setFirstName] = useState(existingContact.firstName || "");
    const [lastName, setLastName] = useState(existingContact.lastName || "");
    const [birthDate, setBirthDate] = useState(existingContact.birthDate || "");
    const [email, setEmail] = useState(existingContact.email || "");
    const [profilePicture, setProfilePicture] = useState(existingContact.profilePicture || "");
    const [isLoggedIn, setIsLoggedIn] = useState(existingContact.isLoggedIn || true);
    const [createdAt, setcreatedAt] = useState(existingContact.createdAt || "");
    const [updatedAt, setUpdatedAt] = useState(existingContact.updatedAt || "");
    const [helping_requests, setHelpingRequests] = useState(existingContact.helping_requests || []);
    
    // if we have an object that has at least one entry inside, then we are updating
    const updating = Object.entries(existingContact).length !== 0

    const onSubmit = async (e) => {
        e.preventDefault()
        // Create a New class User
        // const NewUser = User()


        let num = Math.floor(Math.random() * 100) + 1;
        const data = {
            secretCode: `secret${num}`,
            username: username,
            firstName: firstName,
            lastName: lastName,
            birthDate: birthDate,
            email: email,
            profilePicture: profilePicture,
            rights: 'no',
            isLoggedIn: 'true',
            createdAt: '31/01',
            updatedAt: '31/01',
            helping_requests: 'noo',
            className: 'User'
        }

        console.log(`data object: ${data}`)
        for (const key in data) {
            console.log(`${key}: ${data[key]}`);
            data[key] = await Encryption(data[key]);
            console.log(`${key}: ${data[key]}`);
          }
        // const data = {
        //     firstName,
        //     lastName,
        //     email,
        // }
        //const encrypted_data = EncriptionFernet(data);
        //console.log("encrypted_data: " + encrypted_data)
        const url = "http://127.0.0.1:5000/" + (updating ? `update_contact/${existingContact.id}` : "create_contact" );
        const options = {
            method: updating ? "PATCH" : "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data),
        }
        
        const response = await fetch(url, options)
        console.log(response.status)
        if(response.status !== 201  && response.status !== 200){
            const data = await response.json();
            alert(data.message)
        } else{
            updateCallBackContact();
        }
    }

    

    return <form onSubmit={onSubmit}>
        <div>
            <label htmlFor="username">Username:</label>
            <input 
                type="text" 
                id="username" 
                value={username} 
                onChange={(e) => setUsername(e.target.value)}></input>
        </div>
        <div>
            <label htmlFor="firstName">First Name:</label>
            <input 
                type="text" 
                id="firstName" 
                value={firstName} 
                onChange={(e) => setFirstName(e.target.value)}></input>
        </div>
        <div>
            <label htmlFor="lastName">Last Name:</label>
            <input 
                type="text" 
                id="lastName" 
                value={lastName} 
                onChange={(e) => setLastName(e.target.value)}></input>
        </div>
        <div>
            <label htmlFor="birthDate">birthDate:</label>
            <input 
                type="text" 
                id="birthDate" 
                value={birthDate} 
                onChange={(e) => setBirthDate(e.target.value)}></input>
        </div>
        <div>
            <label htmlFor="email">Email</label>
            <input 
                type="text" 
                id="email" 
                value={email} 
                onChange={(e) => setEmail(e.target.value)}></input>
        </div>
        {/* Change Profile Picture logic LATER!!! */}
        <div>
            <label htmlFor="profilePicture">profilePicture:</label>
            <input 
                type="text" 
                id="profilePicture" 
                value={profilePicture} 
                onChange={(e) => setProfilePicture(e.target.value)}></input>
        </div>
        
        <button type="submit">{updating ? "Update" : "Create"}</button>
    </form>
}

export default ContactForm;