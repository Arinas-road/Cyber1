// need to create a task to the db of the user 
// for teacher - saves to their "requests" db
// for students - saves to their "history of tasks" db 

import react, { useState } from "react"

//updating - value that we get from the previous form


const Task = ({existingTask={}, TaskCallBack }) => {
    const [title, setTitle] = useState("");
    const [date, setDate] = useState("");
    const [time, setTime] = useState("");
    const [location, setLocation] = useState("");
    const [numPeople, setNumPeople] = useState(0); // number of people required
    const [optionalInfo, SetOptionalInfo] = useState("");

    let updating = false;
    if(existingTask) updating = true;

    const ChangeDate = (event) => {
        setDate(new Date(event.target.value)); // Convert string to Date object
      };

    const onSubmit = () => {

    }  
    // + need to get name of a person in the session
    return (
        <form onSubmit={onSubmit}>
        <div>
            <label htmlFor="title">Title:</label>
            <input 
                type="text" 
                id="title" 
                value={title} 
                onChange={(e) => setTitle(e.target.value)}></input>
        </div>
        <div>
            <label htmlFor="date">Date:</label>
            <input 
                type="date" 
                id="date" 
                value={date} 
                onChange={(e) => ChangeDate(e.target.value)}></input>
        </div>
        <div>
            <label htmlFor="time">Time:</label>
            <input 
                type="time" 
                id="time" 
                value={time} 
                onChange={(e) => setTime(e.target.value)}></input>
        </div>
        <div>
            <label htmlFor="location">Location: </label>
            <input 
                type="text"  //maybe change later for another type??????????
                id="location" 
                value={location} 
                onChange={(e) => setLocation(e.target.value)}></input>
        </div>
        <div>
            <label htmlFor="numPeople">Number of people required: </label>
            <input 
                type="number" 
                id="numPeople" 
                value={numPeople} 
                onChange={(e) => setNumPeople(e.target.value)}></input>
        </div>
        <div>
            <label htmlFor="optionalInfo">Optional Info: </label>
            <input 
                type="text" 
                id="optionalInfo" 
                value={optionalInfo} 
                onChange={(e) => SetOptionalInfo(e.target.value)}></input>
        </div>
        <button type="submit">{updating ? "Update" : "Create"}</button>
    </form>
    )
}

export default Task