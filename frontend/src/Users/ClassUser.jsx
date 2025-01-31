import React from 'react'

class ClassUser{
    constructor(
        // Values below are supposed to be entered when the instance is created
        id, // User's ID
        secretCode, // User's secret code from school
        username, // User's username
        firstName, // User's firstname
        lastName, //User's lastname
        birthDate, //User's birthday
        email, // User's email
        profilePicture, // User's profile picture
        rights, // User's rights (what he can access)
        isLoggedIn = true, // See if user is logged in now, by default true
        createdAt, // When user created the account
        updatedAt, // When user updated the account
        helpingRequests = [], // list of his helping requests, by default is an empy list
    ){
        // Set values to the class
        this.id = id;
        this.secretCode = secretCode;
        this.username = username;
        this.firstName = firstName;
        this.lastName = lastName;
        this.birthDate = birthDate;
        this.email = email;
        this.profilePicture = profilePicture;
        this.rights = rights;
        this.isLoggedIn = isLoggedIn;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
        this.helpingRequests = helpingRequests;
    }
    

    //Getters
    GetSecretCode(){return this.secretCode}
    GetUsername(){return this.username}
    GetFirstName(){return this.firstName}
    GetLastName(){return this.lastName}
    GetBirthDate(){return this.birthDate}
    GetEmail(){return this.email}
    GetProfilePicture(){return this.profilePicture}
    GetRights(){return this.rights}
    GetIsLoggedIn(){return this.isLoggedIn}
    GetCreatedAt(){return this.createdAt}
    GetUpdatedAt(){return this.updatedAt}
    GetHelpingRequests(){return this.helpingRequests}


    //Setters
    SetSecretCode(newSecretCode){
        this.secretCode = newSecretCode;
    }
    SetUsername(newUsername){
        this.username = newUsername;
    }
    SetFirstName(newFirstName){
        this.firstName = newFirstName;
    }
    SetLastName(newLastName){
        this.lastName = newLastName;
    }
    SetBirthDate(newBirthDate){
        this.birthDate = newBirthDate;
    }
    SetEmail(newEmail){
        this.email = newEmail;
    }
    SetProfilePicture(newProfilePicture){
        this.profilePicture = newProfilePicture;
    }
    SetRights(newRights){
        this.rights = newRights;
    }
    SetIsLogIn(){
        this.isLoggedIn = true;
    }
    SetCreatedAt(newCreatedAt){
        this.createdAt = newCreatedAt;
    }
    SetUpdatedAt(newUpdatedAt){
        this.updatedAt = newUpdatedAt;
    }
    SetHelpingRequests(newHelpingRequests){
        this.helpingRequests = newHelpingRequests;
    }
    //methods
    //Method receives the helping request that is ccreated by the student
    AddHelpingRequest(newHelpingRequest){
        // the request is pushed to the User's list of helping requests
        this.helping_requests.push(newHelpingRequest);
    }

    //Method receives id of a request that User wants to delete
    RemoveHelpingRequest(requestId){
        //!!!!check later if starting request id 1 or 0!!!!
        //Assuming it's 0:
        // splice(the index from which to start deleting, the number of elements to remove)
        deletedValue = this.helping_requests.splice(requestId, 1);
    }

    //Method allows to return all values of the instance in the json format
    toJSON(){
        return{
            id: this.id,
            secretCode: this.secretCode,
            username: this.username,
            firstName: this.firstName,
            lastName: this.lastName,
            birthDate: this.birthDate,
            email: this.email,
            profilePicture: this.profilePicture,
            rights: this.rights,
            isLoggedIn: this.isLoggedIn,
            createdAt: this.createdAt,
            updatedAt: this.updatedAt,
            helpingRequests: this.helpingRequests,
        };
    }
    
}

// Export ClassUser so we can access it in other files and reaate instances
export default ClassUser;