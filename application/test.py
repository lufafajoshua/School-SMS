import pymysql
from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import VARCHAR, TEXT 
import mysql.connector
from datetime import datetime
from models import Course, db
import os
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import FlaskForm

basedirectory = os.path.abspath(os.path.dirname(__file__))#basedir to use in imageloading


app = Flask(__name__)   

# this userpass assumes you did not create a password for your database
# and the database username is the default, 'root'
userpass = 'mysql+pymysql://joshlufafa:fhdu23AJ8j3hmvbluf@'
basedir  = '127.0.0.1'
# change to YOUR database name, with a slash added as shown
dbname   = '/kyambogosda'
# this socket is going to be very different on a Windows computer
#socket   = '?unix_socket=/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'


# put them all together as a string that shows SQLAlchemy where the database is
app.config['SQLALCHEMY_DATABASE_URI'] = userpass + basedir + dbname

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'Agdgajj938n2!gjjskg@;[pbqbktofd'

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedirectory, 'uploads') # you'll need to create a folder named uploads


db = SQLAlchemy(app)#initialise the database 
# this variable, db, will be used for all SQLAlchemy commands





if __name__ == '__main__':
    app.run(debug=True) 


#migrate = Migrate(app, db) 
    
    # def save(applicant, form, new=False):
    #     applicant.full_name = form.full_name.data
    #     applicant.d_o_birth = form.d_o_birth.data
    #     applicant.gender = form.gender.data
    #     applicant.nationality = form.nationality.data
    #     applicant.age = form.age.data
    #     applicant.m_status = form.m_status.data
    #     applicant.l_o_educ = form.l_o_educ.data
    #     applicant.village = form.village.data
    #     applicant.parish = form.parish.data
    #     applicant.phone_no = form.phone_no.data
    #     applicant.year_of_entry = form.year_of_entry.data
    #     applicant.guardian_name = form.guardian_name.data
    #     applicant.guardian_contact = form.guardian_contact.data
    #     applicant.next_of_kin = form.next_of_kin.data
    #     applicant.next_of_kin_contact = form.next_of_kin_contact.data
    #     applicant.religion = form.religion.data
    #     #Get all the courses form the fromt end that have been selected by the applicant and add to the database
    #     #student = db.relationship('Student', backref='applicant', uselist=False)#Creating a relationship between appicants and accepted students, supply this from the frontend by adding them to the student table
    #     applicant.skills = form.skills.data
    #     applicant.courses = form.courses.data

    #     if new:
    #         db.session.add(applicant)
    #     db.session.commit()

