from flask import Flask, redirect, url_for, escape, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy 
import pymysql.cursors
import pymysql
from models import db, Applicant, Result, Course, Subject, Student, Register_Student, User_Account, Exam_Result, Department, Student_Results, Result, Lecturer, Faculty, Module, Faculty_Member, Department_Member, Course_Requirements, Session, applicant_courses, course_sessions    
from forms import ApplicantForm, ResultForm, AssignCourseForm, CourseForm, DepartmentForm, RequirementsForm, ExamResultForm, SubjectForm
from sqlalchemy.orm import relationship, backref, exc
import os
from sqlalchemy.sql.sqltypes import Integer
import mysql.connector
from flask_migrate import Migrate
from tables import ApplicantTable, CourseTable

app = Flask(__name__)#Instantiate the application

app.config.from_pyfile('school_app.cfg')#Point to the configurations file

db.init_app(app)
#db = SQLAlchemy(app)#Instantiate the database
 
@app.route('/create-course', methods=['GET', 'POST'])#This is added by the Department administrator
def add_course():#Later on use the department id to create the course
    form = CourseForm(request.form)
    if request.method == 'POST':
        course = Course()
        course.title = form.title.data
        course.duration = form.duration.data
        course.course_code = form.course_code.data
        #course.requirements = Course_Requirements(subject_name="History", grade_type="principal")        
        course.cut_off_points = form.cut_off_points.data
        db.session.add(course)
        db.session.commit()
    else:
        form = CourseForm()
    return render_template('add_course.html', form=form) 


@app.route('/all_courses', methods=['GET', 'POST'])
def all_courses():
    qry = db.session.query(Course)
    courses = qry.all()
    table = CourseTable(courses)
    return render_template('all_courses.html', table=table)           

@app.route('/course_detail/<int:id>', methods=['GET', 'POST'])
def course_detail(id):
    qry = db.session.query(Course).filter(Course.id==id)
    course = qry.first()
    form = CourseForm(formdata=None, obj=course)
    return render_template('course.html', form=form, course=course)

@app.route('/apply', methods=['GET', 'POST'])
def applicant():
    form = ApplicantForm(request.form)
    form.courses.choices = [(c.id, c.title) for c in Course.query.all()]
    print(form.courses.choices)
    if request.method == 'POST':
        applicant = Applicant()
        applicant.full_name = form.full_name.data
        applicant.d_o_birth = form.d_o_birth.data
        applicant.gender = form.gender.data
        applicant.nationality = form.nationality.data
        applicant.age = form.age.data
        applicant.m_status = form.m_status.data
        applicant.l_o_educ = form.l_o_educ.data
        applicant.village = form.village.data
        applicant.parish = form.parish.data
        applicant.phone_no = form.phone_no.data
        applicant.year_of_entry = form.year_of_entry.data
        applicant.guardian_name = form.guardian_name.data
        applicant.guardian_contact = form.guardian_contact.data
        applicant.next_of_kin = form.next_of_kin.data
        applicant.next_of_kin_contact = form.next_of_kin_contact.data
        applicant.religion = form.religion.data
        applicant.skills = form.skills.data
        applicant.courses = form.courses.data
        print(applicant.courses)
        db.session.add(applicant)
        db.session.commit()
        for course in form.courses.data:
            selected_course = Course.query.get(course)
            applicant.course.append(selected_course)#Either way the association table will add the related fields to the database
            db.session.commit()
        return redirect(url_for('results', id=applicant.id))        
    return render_template('apply.html', form=form)        

def save_result(result, form, new=False):
    result.former_school = form.former_school.data
    result.index_no = form.index_no.data
    result.total = form.total.data#for now but compute the average points from the results
    #Handle input of subscidiary subjects like computer and Sub math
    if new:
        db.session.add(result)
    db.session.commit()    

@app.route('/applicant_results/<int:id>', methods=['GET', 'POST'])
def results(id):#Use the applicants id to add the results to their profile while applying
    qry = db.session.query(Applicant).filter(Applicant.id==id)
    applicant = qry.first()
    form = ExamResultForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        result = Exam_Result()#Instantiate the result object
        result.former_school = form.former_school.data
        result.index_no = form.index_no.data
        result.total_points = form.total.data#for now but compute the average points from the results
        #result.total_cut_points = 0
        db.session.add(result)
        db.session.commit()
        applicant.result = result#Add the result object to the applicant one to one relationship
        db.session.commit()
        #You can return a redirect to a successfull page once finished with 
        return redirect(url_for('add_subject', id=result.id))
    else:
        form = ExamResultForm()
    return render_template('result.html', form=form)

    # @app.route('/apply_course/<int:applicant_id>', methods=['GET', 'POST'])#Use the applicants id to add the courses they are applying for
    # def apply_course(applicant_id):
        
"""
This is done by the course admin to admit all students who meet with the course requirements
"""
@app.route('/view_applicant/<int:id>', methods=['GET', 'POST'])
def view_applicant(id):
    #Set the various requirements for a student to be admitted into the school 
    #GEt the courses the applicant is applying for
    #Get the applicant results 
    #If the applicant results meet with the course requirements then, add the applicant to the students table and add the first course in the list 
    qry = db.session.query(Applicant).filter(Applicant.id==id)
    applicant = qry.first()
    form = ApplicantForm(formdata=None, obj=applicant)
    courses = applicant.course#This points to the courses selected by the applicant
    results = applicant.result#Results provided by the applicant from their former school
    context = {
        'courses': courses,
        'results': results,
    }
    return render_template('applicant.html', courses=courses, results=results, form=form)

#def assign_reg_no(applicant):#Create the registration number and assign it to the student
    #return a value from the funcion that will be added to the student_reg_no
#def assign_student_no(applicant):#Create the student no and assign it to the student
    #return a value from the ffunction that will be assigned to the student_no

def get_course(applicant):
    courses = applicant.course
    results = applicant.result
    result_points = results.total_cut_points#Get the total points from the result object
    result_subjects = results.subject#Get the results associated witht the result object
    for course in courses:
        subjects = course.requirements.subject_name#Make sure the subject names are consistent with those in the results ie. Provide choices
        cut_points = course.cut_off_points
        #If the result points are >= to the cut_off_points 
        if result_points >= cut_points and subjects in result_subjects: 
            break
        return course.id
    else: 
        return None  
    return redirect(url_for('verification', id=applicant.id))      

@app.route('/auto_admit/<int:id>', methods=['GET', 'POST'])#THis may not use the frontend like html
def auto_admit(id):#USe the id to verify the applicants' results points and also the subjects
    qry = db.session.query(Applicant).filter(Applicant.id==id)
    applicant = qry.first()       
    student = Student()

    courses = applicant.course
    results = applicant.result
    result_points = results.total_cut_points#Get the total points from the result object
    result_subjects = ["{}".format(subject) for subject in results.subject]#results.subject#Get the results associated witht the result object
    if applicant.student_id is not None:
        msg = 'Already added the student'
        #redirect to the student profile with the student_id
        return redirect(url_for('view_applicant', id=applicant.id))
    else:
        for course in courses:
            subjects = ["{}".format(course) for course in course.requirement]#course.requirement#course.requirement.subject_name.all()#Make sure the subject names are consistent with those in the results ie. Provide choices
            cut_points = course.cut_off_points
            #Create a for loop to iterate through the required subjects
            for subject_requirement in subjects:
                if result_points >= cut_points and subject_requirement in result_subjects:#Issues with comparing the subjects 
                    #Return the first course in that meets with these requirements
                    student.course_id = course.id        
                    student.applicant = applicant
                    #student.course_id = course
                    student.reg_num = "16/U/5722/DCS/PE"#assign_reg_no(applicant)# testing first
                    student.student_no = 160708005722#assign_student_no(applicant)#first test this in crating the student object   
                    db.session.add(student)
                    db.session.commit()   

            else: 
                print("Doesnt Qualify")         

    return render_template('auto_admit.html', courses=courses, results=results, applicant=applicant, subjects=subjects, cut_points=cut_points, result_subjects=result_subjects, result_points=result_points)   
                 
#Visually verify the Applicant and then assign a course to them, add this logic directly to the admission module
@app.route('/verification/<int:course_id>')
@app.route('/verification/<int:course_id>/<int:id>', methods=['GET', 'POST'])
def verification(course_id, id=None):#GEt the id of the applicant you are verifying
    qry1 = db.session.query(Applicant).filter(Applicant.id==id)
    applicant = qry1.first()
    qry2 = db.session.query(Course).filter(Course.id==course_id)
    course = qry2.first()
    #GEt the applicant courses 
    courses = applicant.course
    print(courses)
    results = applicant.result
    result_points = results.total_cut_points#Get the total points from the result object
    result_subjects = results.subject#Youcan invoke these from the forntend
    context = {
        'courses': courses,
        'results': results,
        'applicant': applicant,
    }
    return render_template('verification.html', courses=courses, results=results, applicant=applicant, course=course)#return to the admit process

@app.route('/admit/<int:id>/', methods=['GET', 'POST'])
def admit(id):
    qry = db.session.query(Applicant).filter(Applicant.id==id)
    applicant = qry.first()
    #Verify that the applicant is not a student already 
    msg = ''
    courses = applicant.course
    results = applicant.result
    result_points = results.total_cut_points#Get the total points from the result object
    result_subjects = results.subject
    student = Student()
    if applicant.student_id is not None:
        msg = 'Already added the student'
        #redirect to the student profile with the student_id
        return redirect(url_for('view_applicant', id=applicant.id))
    else:
        form = AssignCourseForm(request.form)#Get the assigned course from the frontend
        form.course.choices = [(c.id, c.title) for c in applicant.course]#Get the courses selected by the applicant from the database
        if request.method == 'POST':
            student = Student()
            student.applicant = applicant
            course = form.course.data
            #course = request.form.get('course')
            student.course_id = course#Point to the id returned from selecting the course from the frontend
            student.reg_num = "16/U/5722/DCS/PE"#assign_reg_no(applicant)# testing first
            student.student_no = 160708005722#assign_student_no(applicant)#first test this in crating the student object   
            if student.course_id and student.applicant is not None:
                db.session.add(student)
                db.session.commit()
            else:
                msg = 'Please select the course and then proceed to admit student'    
    context = {
        'applicant': applicant,
        'msg': msg,
        #'form': form,
    }
    return render_template('admit.html', applicant=applicant, form=form, courses=courses, results=results,)

@app.route('/all_applicants', methods=['GET', 'POST'])
def all_applicants():
    qry = db.session.query(Applicant)
    applicants = qry.all()
    table = ApplicantTable(applicants)
    return render_template('all_applicants.html', table=table)

@app.route('/course_admit/<int:course_id>')
@app.route('/course_admit/<int:course_id>/<int:id>', methods=['GET', 'POST'])
def course_admit(course_id, id=None):
    qry1 = db.session.query(Course).filter(Course.id==course_id)
    course = qry1.first()
    qry2 = db.session.query(Applicant).filter(Applicant.id==id)
    applicant = qry2.first()
    if applicant.student_id is not None:
        msg = 'Already added the student'
        #redirect to the student profile with the student_id
        return redirect(url_for('view_applicant', id=applicant.id))
    else:
        student = Student()
        student.applicant = applicant
        student.course_id = course.id
        student.reg_num = "16/U/5722/DCS/PE"
        student.student_no = 160708005722      

        """CReate a default account for the user with student_no as user name and 
        password as reg_no. These can be edited by the user when they have logged in 
        """
        student.user_account = User_Account(username="student_no", password="reg_num")#This will later on be edited by the user to their own liking
        db.session.add(student)
        db.session.commit()
    return render_template('test.html', course=course, applicant=applicant)

@app.route('/course_auto_admit/<int:course_id>')
@app.route('/course_auto_admit/<int:course_id>/<int:id>', methods=['GET', 'POST'])
def course_auto_admit(course_id, id=None):#USe the id to verify the applicants' results points and also the subjects
    
    qry1 = db.session.query(Course).filter(Course.id==course_id)
    course = qry1.first()
    qry2 = db.session.query(Applicant).filter(Applicant.id==id)
    applicant = qry2.first()       
    student = Student() 
    results = applicant.result
    result_points = results.total_cut_points#Get the total points from the result object
    result_subjects = ["{}".format(subject) for subject in results.subject]#results.subject#Get the results associated witht the result object
    if applicant.student_id is not None:
        msg = 'Already added the student'
        #redirect to the student profile with the student_id
        return redirect(url_for('view_applicant', id=applicant.id))
    else:    
        subjects = ["{}".format(course) for course in course.requirement]#course.requirement#course.requirement.subject_name.all()#Make sure the subject names are consistent with those in the results ie. Provide choices
        cut_points = course.cut_off_points
        #Create a for loop to iterate through the required subjects
        for subject_requirement in subjects:
            if result_points >= cut_points and subject_requirement in result_subjects:#Issues with comparing the subjects 
                #Return the first course in that meets with these requirements
                student.course_id = course.id        
                student.applicant = applicant
                #student.course_id = course
                student.reg_num = "16/U/5722/DCS/PE"#assign_reg_no(applicant)# testing first
                student.student_no = 160708005722#assign_student_no(applicant)#first test this in crating the student object   
                db.session.add(student)
                db.session.commit()   

        else: 
            print("Doesnt Qualify")         

    return render_template('course_auto_admit.html', course=course, results=results, applicant=applicant, subjects=subjects, cut_points=cut_points, result_subjects=result_subjects, result_points=result_points)

@app.route('/subject/<int:id>', methods=['GET', 'POST'])
def add_subject(id):#
    qry = db.session.query(Exam_Result).filter(Exam_Result.id==id)
    result = qry.first()
    #Get all the subjects in the database and if they exceed 5, return error or exit
    qry_subjects = db.session.query(Subject)
    all_subjects = len(result.subject)#Count all the sujects available in the system
    msg = ''
    form = SubjectForm(request.form)
    #If the number of subjects is greater than 5 return an error message
    if all_subjects == int(4):
        msg = 'subjects exceeded the required number'
        return redirect(url_for('applicant'))
        return msg
    else:    
        if request.method == 'POST':
            subject = Subject()
            subject.subject_name = form.subject_name.data
            subject.grade = form.grade.data
            if subject.grade == "A":
                result.total_cut_points += 4.5#GEt the default from the database and add it to the points associated with a grade
            elif subject.grade == "B":
                result.total_cut_points += 4.0
            elif subject.grade == "C":
                result.total_cut_points += 3.5 
            elif subject.grade == "D":
                result.total_cut_points += 3.0
            elif subject.grade == "E":
                result.total_cut_points += 2.5   
            elif subject.grade == "F":
                result.total_cut_points += 0#If the subject is being deleted. Delete also its points from the cut_off points              
            db.session.add(subject)
            db.session.commit()
            #result.total_cut_points = sum([subject for subject in subject.cut_points])
            subject.result_id = result.id#Point to the result_id in the subject table
            db.session.commit()
            #COmpute the total points from the result objects
            #Return to the same page inorder to add another subject and score
            #If the subject instances are more than a given number, redirect to another page
            return redirect(url_for('add_subject', id=result.id))#Let the user add other subjects and not just one
        else:
            form = SubjectForm()
    return render_template('add_subject.html', form=form, result=result, msg=msg)        

#This is a test view
@app.route('/assign_course/<int:applicant_id>', methods=['GET', 'POST'])
def assign_course(applicant_id):
    qry = db.session.query(Applicant).filter(Applicant.id==applicant_id)
    applicant = qry.first()
    applicant_points = appplicant.result.total_points
    form = AssignForm(request.form)
    if request.method == 'POST':
        for course in applicant.courses:
            if applicant_points >= course.cut_off_points:
                return course
    else:
        form = AssignForm() 
    return render_template('assign.html', form=form)               

@app.route('/create_department', methods=['GET', 'POST'])
def create_department():
    department = Department()
    form = DepartmentForm()
    if request.method == 'POST' and form.validate_on_submit():
        department.name = form.name.data

@app.route('/add_requirements/<int:id>', methods=['GET', 'POST'])
def add_requirements(id):
    qry = db.session.query(Course).filter(Course.id==id)
    course = qry.first()
    form = RequirementsForm()
    if request.method == 'POST':
        requirement = Course_Requirements()
        requirement.subject_name = form.subject_name.data
        requirement.grade_type = form.grade_type.data
        db.session.add(requirement)
        db.session.commit()
        requirement.course_id = course.id 
        db.session.commit()
    return render_template('requirements.html', form=form, course=course)    

@app.route('/add_module/<int:course_id>', methods=['GET', 'POST'])
def add_module(course_id):
    qry = db.session.query(Course).filter(Course.id==Course_id)
    course = qry.first()
    form = ModuleForm(request.form)
    if request.method == 'POST':
        module = Module()
        module.module_code = form.module_code.data
        module.title = form.title.data
        db.session.add(module)
        db.session.commit()
        course.modules.add(module)
    else:
        form = ModuleForm()
    return render_template('module.html', course=course, form=form)        

    #Use student.student.add(applicant)db.session.add(applicant)
    #provide all the necessary information about the student and then save it or commit the changes to the database

@app.route('/all_results', methods=['GET', 'POST'])
def add_results():
    all_results = Student_Results()
    return render_template('all_results.html')

@app.route('/all_students', methods=['GET', 'POST'])
def all_students():
    qry = db.session.query(Student)
    students = qry.all()
    return render_template('all_students.html', students=students)

@app.route('/view_student/<int:id>', methods=['GET', 'POST'])
def view_student(id):
    #Set the various requirements for a student to be admitted into the school 
    #GEt the courses the applicant is applying for
    #Get the applicant results 
    #If the applicant results meet with the course requirements then, add the applicant to the students table and add the first course in the list 
    qry = db.session.query(Student).filter(Student.id==id)
    student = qry.first()
    
   
    return render_template('student.html', student=student)

with app.app_context():
    db.create_all() # change the storage engine to InnoDB  
if __name__ == '__main__':
    app.run(debug=True)







             




          


