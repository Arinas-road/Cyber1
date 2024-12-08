import {useState} from "react"

const ContactForm = ({existingContact={}, updateCallBack}) => {
    const [firstName, setFirstName] = useState(existingContact.firstName || "");
    const [lastName, setLastName] = useState(existingContact.lastName || "");
    const [email, setEmail] = useState(existingContact.email || "");

    // if we have an object that has at least one entry inside, then we are updating
    const updating = Object.entries(existingContact).length !== 0

    const onSubmit = async (e) => {
        e.preventDefault()

        const data = {
            firstName,
            lastName,
            email,
        }
        const url = "http://127.0.0.1:5000/" + (updating ? `update_contact/${existingContact.id}` : "create_contact" );
        const options = {
            method: updating ? "PATCH" : "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data),
        }
        console.log("AAA")
        const response = await fetch(url, options)
        console.log(response.status)
        if(response.status !== 201  && response.status !== 200){
            const data = await response.json();
            alert(data.message)
        } else{
            updateCallBack();
        }
    }

    

    return <form onSubmit={onSubmit}>
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
            <label htmlFor="email">Email</label>
            <input 
                type="text" 
                id="email" 
                value={email} 
                onChange={(e) => setEmail(e.target.value)}></input>
        </div>
        <button type="submit">{updating ? "Update" : "Create"}</button>
    </form>
}

export default ContactForm;