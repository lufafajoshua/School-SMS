from operator import itemgetter, attrgetter
import datetime
import itertools
from array import *

 
class Parent:
    def __init__(self, name, Occupation, email, telephone):
        self.name = name
        self.email = email
        self.occupation = Occupation
        self.telephone = telephone

class Teacher(Parent):
    def __init__(self, title):
        self.title = title
    def comment(result):#Function takes in the student average as its input and return a string to comment to the students performance
        if result >= 80: return "Excellent"
        elif result >= 60: return "Good"
        elif result >= 50: return "Good trial, More efforts needed"
        elif result >= 30: return "Try marriage"
        else: return "Poor, performance. get serious with your books"


parent = Parent("Luwedde Joan", "lufafajoshua@gmail.com", "Farmer", "0787579789")
teacher = Teacher("class Teacher")

class Student(object):
    #Class attribute
    id_generator = itertools.count(1021) 
    def __init__(self, name, age, stream, sex, nationality, date_of_birth):
        self.name = name
        self.age = age
        self.stream = stream
        self.sex = sex
        self.nationality = nationality
        self.date_of_birth = date_of_birth
        self.id = next(self.id_generator)
    #str() function to format output of the student identity number  
    def __str__(self):
        return "16/U/{}/DCS/PE".format(self.id) 
    def assign_marks(self):
        marks = []
        def input_number(msg, err_msg=None):
            while True:
                try:
                    return float(input(msg))
                except ValueError:
                    if err_msg is not None:
                        print(err_msg)
        subjects = ['Maths', 'History', 'Chemistry', 'Computer']
        for i in subjects:
            k = int(input_number("Enter mark for %s:\n" %(i), "That is not a number"))
            marks.append(k)
            my_results = (array('i'))
            my_results.fromlist(marks)

        def get_average(results):# This function is to be called by another function in the same class
            total_sum =  sum(results)
            total_sum = float(total_sum)
            return  total_sum / len(results)

        def assign_letter_grade(score):#LAso to be called within this class
            if score >= 90: return "A"
            elif score >= 80: return "B"
            elif score >= 70: return "C"
            elif score >= 60: return "D"
            elif score >= 50: return "E"
            else: return "F"
        
        for a, b in zip(subjects, marks):#appending and printing the subjects list and the marks list
            print(a, b)
        for x in my_results:#Iterating through the results list while assigning grades to the marks
            print(assign_letter_grade(x))

        Average_mark = get_average(my_results) 
        print("Average:", Average_mark)

#Create student objects and plaicing them in alist
s1 = Student("Lufafa", 24, "Blue", "Male", "Ugandan", datetime.date(1945, 4, 4))
s2 = Student("Nambi", 34, "Yellow", "Female", "Ugandan", datetime.date(1994, 9, 12))
s3 = Student("kikomeko", 56, "Green", "Male", "Kenyan", datetime.date(1967, 3, 11))
s1.assign_marks()
print(s1)
#l = [s1, s2, s3]
             




            