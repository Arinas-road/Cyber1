import { useState, useEffect, useRef } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'

// components for rendering
import ContactList from './ContactList'
import ContactForm from './ContactForm'
import Task from './Task'

import './App.css'




function App() {
  // store our contacts
  const [contacts, setContacts] = useState([]);
  const [isContactOpen, setIsContactOpen] = useState(false);
  const[currentContact, setCurrentContact] = useState({});
  // const ws = useRef(null);

  // useEffect(() => {
  //   ws.current = new WebSocket('ws://127.0.0.1:5000'); // Replace with your server's address
  //   console.log('Websocket created');
  //   ws.current.onopen = () => {
  //     console.log('WebSocket connected');
  //     const testData = {
  //       command: "create_contact",
  //       firstName: "John",
  //       lastName: "Doe",
  //       email: "john.doe@example.com"
  //     };
  //     ws.current.send(JSON.stringify(testData));  // Send the command to the server
   
  //   };

  //   ws.current.onmessage = (event) => {
  //     console.log("Received message from server: ", event.data);
  //     // Parse the server's response if needed
  //     const response = JSON.parse(event.data);
  //     console.log(`Response from server: ${response}`)
  //   };

  //   ws.current.onclose = () => {
  //     console.log('WebSocket closed');
  //   };

  //   // return () => {
  //   //   if (ws.current) {
  //   //     ws.current.close();
  //   //   }
  //   // };
  // }, []);

  // we want to call fetch contacts once, after initial render
  useEffect(() => {
    fetchContacts()
  }, [])

  // send requests to the backend to get the contacts
  const fetchContacts = async () => {
    const response = await fetch('http://127.0.0.1:5000/contacts');
    const data = await response.json(); // returns {"contacts": []}
    // updates our contacts variable
    setContacts(data.contacts);
    console.log(data.contacts)
  }
  // function for toggling the ContactForm
  const closeContact = () => {
    setIsContactOpen(false);
    setCurrentContact({});
  }
  const openCreateContact = () => {
    if(!isContactOpen) setIsContactOpen(true)
  }

  const openEditContact = (contact) => {
    if(isContactOpen) return;
    setCurrentContact(contact);
    setIsContactOpen(true);
  }

  const onUpdate = () => {
    closeContact();
    fetchContacts();
  }

  

  return (
    <>
      <ContactList contacts={contacts} updateContact={openEditContact} updateCallBackContact={onUpdate}/>
      <button onClick={openCreateContact}>Create New Contact</button>
      {
        isContactOpen && <div className='modal'>
          <div className='modal-content'>
            <span className='close' onClick={closeContact}>&times;</span>
            <ContactForm existingContact={currentContact} updateCallBackContact={onUpdate}/>
          </div>
        </div>
      }
      <Task existingTask={""} TaskCallBack={""}></Task>
      
    </>
  )
}

export default App
