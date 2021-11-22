
applicant_courses = db.Table('applicant_courses',
    #db.Column('id', db.Integer, primary_key=True),
    db.Column('applicant_id', db.Integer, db.ForeignKey('applicant_data.id', ondelete="cascade")),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id', ondelete="cascade"))
) 

class Applicant(db.Model):#This will be used to store data for students who are applying for a course
    __tablename__ = 'applicant_data'

    id = db.Column(db.Integer, primary_key=True)#First define the unique key for every object to be passed
    full_name = db.Column(db.String(128), unique=False, nullable=False)#Some schools may split the name into firstname and last name
    image_file = db.Column(db.String(120), index=False, nullable=True, default="noavatar92.png")#Remove it and add it to the student object
    d_o_birth = db.Column(db.DateTime, index=True, nullable=False)
    gender = db.Column(db.String(100), index=True, nullable=False)
    nationality = db.Column(db.String(120), index=True, nullable=False)
    age = db.Column(db.Integer, index=True, nullable=False) 
    m_status = db.Column(db.String(128), index=True, nullable=False)
    l_o_educ = db.Column(db.String(128), index=False, nullable=False)#level of education
    village = db.Column(db.String(120), index=False, nullable=False)
    parish = db.Column(db.String(120), index=False, nullable=False)
    phone_no = db.Column(db.String(100), index=False, nullable=True)
    year_of_entry = db.Column(db.Integer, index=True, nullable=False)
    guardian_name = db.Column(db.String(200), index=True, nullable=False)#This can also be used to refer to both mother and mother
    guardian_contact = db.Column(db.String(200), index=True, nullable=False)
    next_of_kin = db.Column(db.String(200), index=True, nullable=False)#Name of next of kin
    next_of_kin_contact = db.Column(db.String(200), index=True, nullable=False)
    religion = db.Column(db.String(120), index=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))#This will store the student id from the applicants table, id of the applicant accepted in the
    skills = db.Column(db.Text, index=False, nullable=True)
    result = db.relationship('Exam_Result', backref='applicant_results', uselist=False)#One applicant has only one result object from the previous examinations
    course = db.relationship('Course', secondary=applicant_courses, lazy='subquery', backref=db.backref('applicant_data', lazy=True))#Define a many-to-many relationship. Applicant applies for one or many courses and a course is applied for by one or many applicants

class Exam_Result(db.Model):#Results obtained from the previous exams beig used as entry exams ie UNEB 
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)#This primary key is associated with the student object beig used in application via a one to one relationship
    former_school = db.Column(db.String(200), index=True, nullable=False)
    index_no = db.Column(db.String(120), index=True, nullable=False) 
    subject = db.relationship('Subject', backref='subjectresult')#One to many with asubject table ie One result object has many subject results
    total_points = db.Column(db.Integer, index=False, nullable=False)#Calculate the total number of points from the system
    total_cut_points = db.Column(db.Float, nullable=False, default=0)#Get a summation of all the subject cut_off points and add them altogether
    applicant = db.Column(db.Integer, db.ForeignKey('applicant_data.id'))
    #Add another field to handle the total points to be used in cut_off_points
    #all_results_id = db.Column(db.Integer, db.ForeignKey('student_results.id'))   

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(120), index=True, nullable=False)#This is the subject name and then down you add the result   
    grade = db.Column(db.String(10), index=False, nullable=False)#Compute the grade points in the frontend ie while calculating the total points 
    #cut_points = db.Column(db.Float, index=False, nullable=False, default=0)#Provide a summation of each of the points to be used in cut_off points
    result_id = db.Column(db.Integer, db.ForeignKey('results.id'))

    def __repr__(self):
        return self.subject_name 

#Create a table to handle students who have been fully accepted by the University and have been given Courses to do
class Student(db.Model):
    __tablename__ = 'students'#This is the students_table to hold their data

    id = db.Column(db.Integer, primary_key=True)
    """ A one to one relationship between student and applicant. An accepted applicant is refrenced to by this relationship""" 
    applicant = db.relationship('Applicant', backref='students', uselist=False)#One student is one applicant
    department = db.relationship('Department', backref='department_students', uselist=False)#Provide it via the course department, one student belongs to only one department 
    reg_num = db.Column(db.String(78), index=True, nullable=False)#You can use this as the login for the first time the user is using their portal
    student_no = db.Column(db.Integer, index=True, nullable=False)#This will be used in login   
    user_account = db.relationship('User_Account', backref='user_account', uselist=False)
    result_id = db.Column(db.Integer, db.ForeignKey('exam_results.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))#specify the course that a student is offering or that is being assigned
    all_results = db.Column(db.Integer, db.ForeignKey('student_results.id'))
    register = db.relationship('Register_Student', backref='student_status')#A One to many with the. if the student has registered for a session. return an error 

course_sessions = db.Table('course_sessions',
    #db.Column('id', db.Integer, primary_key=True),
    db.Column('session_id', db.Integer, db.ForeignKey('session.id', ondelete="cascade")),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id', ondelete="cascade"))
) 

class Session(db.Model):
    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, index=True, nullable=False)#The year and semister will be used in registering
    semister = db.Column(db.Integer, index=True, nullable=False)
    status = db.Column(db.Boolean, index=True, nullable=False)#Its either active or closed
    reg_students = db.relationship('Register_Student', backref='registered')#This handles all registered students for a particular session
    student_results = db.relationship('Student_Results', backref='student_results')#One session has many student results
    modules = db.relationship('Module', backref='modules')#The modules to be done in this session, one session has many modules to be done in it
    session_results = db.Column(db.Integer, db.ForeignKey('student_results.id'))

class Course(db.Model):
    __tablename__ = 'courses'
     
    id = db.Column(db.Integer, primary_key=True)#Each course offered at the  institution has an id which will be given to a student when fully accepted
    title = db.Column(db.String(250), index=False, nullable=False)
    duration = db.Column(db.Integer, index=False, nullable=False)
    course_code = db.Column(db.String(100), index=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    cut_off_points = db.Column(db.Float, index=True, nullable=False)#USed for applicants admission 
    sessions = db.relationship('Session', secondary=course_sessions, lazy='subquery', backref=db.backref('course', lazy=True))
    requirement = db.relationship('Course_Requirements', backref='course')
    modules = db.relationship('Module', backref='course')#Define a many-to-many relationship between acourse and the modulels. A course has many modules and many modules belong to more than one Course
    students = db.relationship('Student', backref='course_students')#A Course has many students and a student offers only on ecourse
    all_results_id = db.Column(db.Integer, db.ForeignKey('student_results.id'))#Access results for a course via a session 

    def __repr__(self):
        return '<Course {}>'.format(self.title)     
"""
This data is to be used in assignibg a course to a student given particular rewuirements
"""
class Course_Requirements(db.Model):#One can have one to many requirements relationship witht the 
    __tablename__ = 'course_requirements'

    id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(120), index=False, nullable=False)
    grade_type = db.Column(db.String(10), index=False, nullable=False)#it can represent a principal pass, which denotes anything between A->E, you can ommit this if it isnt neccessary 
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))#Foreign key to the course table

    def __repr__(self):
        return self.subject_name 

class Module(db.Model):
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    module_code = db.Column(db.String(180), index=True, nullable=False)
    title = db.Column(db.String(128), index=True, nullable=False)
    result_id = db.Column(db.Integer, db.ForeignKey('exam_results.id'))#points to the marks obtained from the the exams in this module
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturers.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))#When is the module to be done
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))


class Register_Student(db.Model):#This is a table for a registered student, attach th course being registered for 
    __tablename__ = 'regestered_students'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))#One student registers and is doing one course
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))#Foreign key to the student object, A one to many with the many students regestering for one session and one course
    session = db.Column(db.Integer, db.ForeignKey('session.id'))
    status = db.Column(db.Boolean, nullable=False)#You can create a table for the status of the student
    reg_id = db.Column(db.Integer, nullable=False)#Attach a reg id to each student who has regestered for a semister, generate one for the student

class User_Account(db.Model):
    __tablename__ = 'user_account'

    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(128), index=False, nullable=False)#Used for login to the portal
    password = db.Column(db.String(128), index=False, nullable=False)#Used in student authentication   
    students = db.Column(db.Integer, db.ForeignKey('students.id'))#One User has only one user_account
    #Enable the use of the student number in authentication

class Result(db.Model):#This handles results obtained in aprticular module by the students
    __tablename__ = 'exam_results'

    id = db.Column(db.Integer, primary_key=True)
    student = db.relationship('Student', backref='module_result')#One
    module = db.relationship('Module', backref='results', uselist=False)#One module has many student results
    test = db.Column(db.Integer, index=True, nullable=False)#Shouldnt go beyond the maximum
    course_work = db.Column(db.Integer, index=True, nullable=False)#Shouldnt go beyonf the maximum
    exam = db.Column(db.Integer, index=True, nullable=False)
    total = db.Column(db.Integer, index=True, nullable=False)#Total shouldnt exceed 100 as maximum
    cgpa = db.Column(db.Float, index=True, nullable=False)# how to represent decimal values in models This is the average from the obtained results, if it goes beyond the maximum ie 5, return error
    all_results = db.Column(db.Integer, db.ForeignKey('student_results.id'))#Access all the student results from the results backref

class Student_Results(db.Model):#Get all the module results belonging to a student
    __tablename__ = 'student_results'

    id = db.Column(db.Integer, primary_key=True)
    module_result = db.relationship('Result', backref='student-results')#A student result has many module results
    student = db.relationship('Student', backref='results', uselist=False)#
    course = db.relationship('Course', backref='results')##One course has many student results
    session = db.relationship('Session', backref='all_results', uselist=False)#These results belog to a single session
    
class Lecturer(db.Model):
    __tablename__ = 'lecturers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    phone_no = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    course_module = db.relationship('Module', backref='lecturer_modules')#One lecturer can handle many course modules, consider changing to one to one if possible
    date_joined = db.Column(db.DateTime, index=False, nullable=False)
    department = db.relationship('Department', backref='department')#One lecturer can belong to one or many departments
    #user_account = db.relationship('User_Account', backref='user_account', uselist=False)#One lecturer has only one user accountand one account belongs to one lecturer
    #photo=#include the lecturers photo

#Table for joing the members to different departments
departmentals = db.Table('departmentals',
    #db.Column('id', db.Integer, primary_key=True),
    db.Column('member_id', db.Integer, db.ForeignKey('department_members.id', ondelete="cascade")),
    db.Column('department_id', db.Integer, db.ForeignKey('department.id', ondelete="cascade"))
)

class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    faculty = db.Column(db.Integer, db.ForeignKey('faculty.id'))#One faculty has many departments
    courses = db.relationship('Course', backref='department')
    members = db.relationship('Department_Member', secondary=departmentals, lazy='subquery', backref=db.backref('department_member', lazy=True))
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturers.id'))
    students = db.Column(db.Integer, db.ForeignKey('students.id'))

class Department_Member(db.Model):   #Members who may not be part of the teaching staff 
    __tablename__ = 'department_members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    position = db.Column(db.String(128), unique=False, nullable=False)
    phone_no = db.Column(db.String(128), unique=False, nullable=False)
    email = db.Column(db.String(128), unique=False, nullable=False)

faculty_members = db.Table('faculty_members',
    #db.Column('id', db.Integer, primary_key=True),
    db.Column('member_id', db.Integer, db.ForeignKey('fac_member.id', ondelete="cascade")),
    db.Column('faculty_id', db.Integer, db.ForeignKey('faculty.id', ondelete="cascade"))
)

class Faculty(db.Model):
    __tablename__ = 'faculty'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    members = db.relationship('Faculty_Member', secondary=faculty_members, lazy='subquery', backref=db.backref('members', lazy=True))#Create a relationship between the member object and the FAculty
    departments = db.relationship('Department', backref='faculty_departments')#One faculty has many departments, many departments belong to one faculty

class Faculty_Member(db.Model):
    __tablename__ = 'fac_member'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    position = db.Column(db.String(128), unique=False, nullable=False)
    email = db.Column(db.String(128), unique=False, nullable=False)
    phone_no = db.Column(db.String(128), unique=False, nullable=False)
