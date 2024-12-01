import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'

// components for rendering
import ContactList from './ContactList'
import ContactForm from './ContactForm'

import './App.css'




function App() {
  // store our contacts
  const [contacts, setContacts] = useState([])
  const [isModalOpen, setIsModalOpen] = useState(false)

  // we want to call fetch contacts once, after initial render
  useEffect(() => {
    fetchContacts()
  }, [])

  // send requests to the backend to get the contacts
  const fetchContacts = async () => {
    const response = await fetch("http://127.0.0.1:5000/contacts");
    const data = await response.json(); // returns {"contacts": []}
    // updates our contacts variable
    setContacts(data.contacts);
    console.log(data.contacts)
  }
  // function for toggling the Modal
  const closeModal = () => {
    setIsModalOpen(false);
  }
  const openCreateModal = () => {
    if(!isModalOpen) setIsModalOpen(true)
  }
  return (
    <>
      <ContactList contacts={contacts}/>
      <button onClick={openCreateModal}>Create New Contact</button>
      {
        isModalOpen && <div className='modal'>
          <div className='modal-content'>
            <span className='close' onClick={closeModal}>&times;</span>
            <ContactForm/>
          </div>
        </div>
      }
      
    </>
  )
}

export default App
