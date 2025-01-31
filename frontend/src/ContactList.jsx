// here will be components for rendering 

import React from "react"

const ContactList = ({contacts, updateContact, updateCallBackContact}) => {

    const onDelete = async (id) => {
        try{
            const options = {
                method: "DELETE"
            }
            const response = await fetch(`http://127.0.0.1:5000/delete_contact/${id}`, options);
            if(response.status === 200){
                updateCallBackContact();
            } else{
                console.error("Failed to Delete");
            }
        } catch (error){
            alert(error);
        }
    }

    return <div>
        <h2>Contacts</h2>
        <table>
            <thead>
                <tr>
                    <th>Username</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>BirthDate</th>
                    <th>Email</th>
                    <th>ProfilePicture</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {contacts.map((contact) => (
                    <tr key={contact.id}>
                        <td>{contact.username}</td>
                        <td>{contact.firstName}</td>
                        <td>{contact.lastName}</td>
                        <td>{contact.birthDate}</td>
                        <td>{contact.email}</td>
                        <td>{contact.profilePicture}</td>
                        <td>
                            <button onClick={() => updateContact(contact)}>Update</button>
                            <button onClick={() => onDelete(contact.id)}>Delete</button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
}

export default ContactList