import classUser from "./ClassUser";

class classStudent extends classUser{
    constructor(props, StudyingInGrade, specialSkills){
        super(props);
        this.StudyingInGrade = StudyingInGrade;
        this.specialSkills = specialSkills;
        this.className = "Student";
    }

    //Getters
    GetGrade(){return this.grade}
    GetSpecialSkils(){return this.specialskills}
    GetClassName(){return this.className}
    //Setters
    SetGrade(newStudyingInGrade){
        this.StudyingInGrade = newStudyingInGrade;
    }
    SetSpecialSkills(newSpecialSkills){
        this.specialSkills = newSpecialSkills;
    }
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
            StudyingInGrade: this.StudyingInGrade,
            specialSkills: this.specialSkills,
            className: this.className,
        };
    }
}

export default classStudent