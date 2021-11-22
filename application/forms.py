from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, RadioField, DateField, FileField, SelectMultipleField, widgets, FormField, IntegerField, SelectField, BooleanField, FormField, FieldList, FloatField
from wtforms.validators import DataRequired, Length, Email
from wtforms import validators
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from models import Department, Course 

class ApplicantForm(FlaskForm):
    full_name = StringField('Full name', [DataRequired()])
    d_o_birth = DateField('Date Of Birth')
    gender = RadioField('Gender', [DataRequired()], choices=[('Male', 'Male'), ('Female', 'Female')])
    nationality = StringField('Nationality', [DataRequired()])
    age = IntegerField('Age', [DataRequired()]) 
    m_status = RadioField('Marital Status', [DataRequired()], choices=[('single', 'Single'), ('married', 'Married')])
    l_o_educ = SelectField('Level of Education', choices=[('primary', 'Primary'), ('secondary', 'Secondary'), ('university', 'University')])
    village = StringField('Village', [DataRequired()])
    parish = StringField('Parish', [DataRequired()])
    phone_no = StringField('Telephone Contact')
    year_of_entry = IntegerField('Year Of Entry')
    guardian_name = StringField('Guardian name', [DataRequired()])
    guardian_contact = StringField('Guardian Contact')
    next_of_kin = StringField('Next of Kin', [DataRequired()])
    next_of_kin_contact = StringField('Telephone Contact')
    religion = StringField('Religion')
    skills = TextAreaField('Skills')
    
    courses = SelectMultipleField('Courses', coerce=int, widget=widgets.ListWidget(prefix_label=True), option_widget=widgets.CheckboxInput())

    def set_choices(self):
        self.courses.choices = [(d.id, d.title) for d in Course.query.all()]

class ExamResultForm(FlaskForm):
    former_school = StringField('Former School', [DataRequired()])
    index_no = StringField('Index Number', [DataRequired()])#Set it to a format for consitency
    total = IntegerField('Total', [DataRequired()])
    #Provide the gradetype via the the frontend

class CourseForm(FlaskForm):
    title = StringField('Course Title', [DataRequired()])
    duration = IntegerField('Duration', [DataRequired()])
    course_code = StringField('Course Code', [DataRequired()])
    cut_off_points = FloatField('Cut off Points', [DataRequired()])

class RequirementsForm(FlaskForm):
    subject_name = StringField('Subject', [DataRequired()])
    grade_type = SelectField('Grade Type', choices=[('principal', 'principal'), ('pass', 'pass')])
    #cut_off_points = FloatField('Cut Off Points')

class ModuleForm(FlaskForm):
    module_code = StringField('Code', [DataRequired()]) 
    title = StringField('Title', [DataRequired()])      

class SemisterForm(FlaskForm):
    semister_no = IntegerField('Semister', [DataRequired()])    

class SessionForm(FlaskForm):
    year = IntegerField('Year', [DataRequired()])
    status = BooleanField('Status', [DataRequired()])

class RegistrationForm(FlaskForm):
    status = BooleanField('Status', [DataRequired()])#The status of the student, either registered or not, Yes/No
    #Provide the registration id from the views ie generate one for ths student

class UserForm(FlaskForm):
    username = StringField('User Name', [DataRequired()])
    password = StringField('Password', [DataRequired()])
    category = SelectField('Category', choices=[('Student', 'student'), ('lecturer', 'lecturer')])#This defines the category of the user#The lecturere has to enter a lecturer id for logging in

class ResultForm(FlaskForm):
    test = IntegerField('Test')#Some forms may be empty 
    course_work = IntegerField('Course Work')
    exam = IntegerField('Exam')
    #Compute the total and the cgpa fom the views and attach them to the result

class LecturerForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    phone_no = StringField('Telephone Contact', [DataRequired()])
    email = StringField('Email', validators=[Email()])#One may not have an email address as such
    departments = SelectMultipleField('Department', coerce=int,  widget=widgets.ListWidget(prefix_label=True), option_widget=widgets.CheckboxInput())
    
class DepartmentForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    members = SelectMultipleField('Department_Member', coerce=int,  widget=widgets.ListWidget(prefix_label=True), option_widget=widgets.CheckboxInput())

class MemberForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    position = SelectField('Position', choices=[('head', 'Head'), ('secretary', 'Secretary'), ('treasurer', 'Treasurer'), ('administrator', 'Administrator'), ('communications', 'Communications')])
    phone_no = StringField('Telephone Contact', [DataRequired()])
    email = StringField('Email', validators=[Email()])

class FacultyForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    members = SelectMultipleField('Faculty_Member', coerce=int,  widget=widgets.ListWidget(prefix_label=True), option_widget=widgets.CheckboxInput())

class FacultyMemberForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    position = SelectField('Position', choices=[('head', 'Head'), ('secretary', 'Secretary'), ('treasurer', 'Treasurer'), ('administrator', 'Administrator'), ('communications', 'Communications')])
    phone_no = StringField('Telephone Contact', [DataRequired()])
    email = StringField('Email', validators=[Email()])

class SubjectForm(FlaskForm):
    subject_name = StringField('Subject Name', [DataRequired()])
    grade = StringField('Grade', [DataRequired()])

class AssignCourseForm(FlaskForm):
    course = RadioField('Select Course', coerce=int)#provide the values from the courses selected by the applicant



