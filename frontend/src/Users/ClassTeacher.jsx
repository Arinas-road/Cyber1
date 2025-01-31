import classUser from "./ClassUser";
class classTeacher extends classUser{
    constructor(props, subjectsTeaching, gradesTeaching){
        super(props);
        this.subjectsTeaching = subjectsTeaching;
        this.gradesTeaching = gradesTeaching;
        this.className = "Teacher";
    }
    //Getters
    GetSubject(){return this.subjects}
    GetGrades(){return this.grades}
    GetClassName(){return this.className}
    //Setters
    SetSubject(newSubjectsTeaching){
        this.subjectsTeaching = newSubjectsTeaching;
    }
    SetGrades(newGradesTeaching){
        this.gradesTeaching = newGradesTeaching;
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
            subjectsTeaching: this.subjectsTeaching,
            gradesTeaching: this.gradesTeaching,
            className: this.className,
        };
    }
}

export default classTeacher;