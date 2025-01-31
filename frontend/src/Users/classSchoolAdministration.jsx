import classUser from "./ClassUser";

class classSchoolAdministartion extends classUser{
    constructor(props){
        super(props)
        this.className = "Administartion";
    }

    //Getters
    GetClassName(){return this.className};
    //methods
    toJSON(){
        return {
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
            className: this.className,
        };
    }
}

export default classSchoolAdministartion;