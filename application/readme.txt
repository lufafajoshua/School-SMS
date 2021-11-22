database details
database name = schoolsystem
username = lufafajosh
password = daffghafwv43"$fdhjj


#This uses automatic admission for the students, This is code to automatically admit the applicant into the school
@app.route('/test_admit/<int:applicant_id>', methods=['GET', 'POST'])
def test_admit(applicant_id):
    qry = db.session.query(Applicant).filter(Applicant.id==applicant_id)
    applicant = qry.first()
    courses = applicant.courses#This points to the courses selected by the applicant
    results = applicant.result#Results provided by the applicant from their former school
    #compare the result

    for course in courses:
        requirements = course.requirements
        for requirement in requirements:
            if requirement.subject_name in results.subject_name.all() and requirement.grade_type in results.grade_type.all():
                #Create the student object here, but for tsting print("Successfull")
                print("Successful")
            else:
                print("Not successful") 
        if results.total_points >= course.cut_off_points:
            return course
        else:
            print("Cant find any")    

    return render_template('test.html')  