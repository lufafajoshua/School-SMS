from flask_table import Table, Col, LinkCol, ButtonCol

"""
Display all the applicants by this data
"""
class ApplicantTable(Table):
    id = Col('id', show=False)
    full_name = Col('Full name')
    gender = Col('Gender')
    nationality = Col('Nationality', show=False)
    profile = LinkCol('View Profile', 'view_applicant', url_kwargs=dict(id='id'))
    admit = LinkCol('Admit', 'admit', url_kwargs=dict(id='id'))
    auto_admit = LinkCol('Auto Admit', 'auto_admit', url_kwargs=dict(id='id'))

class CourseTable(Table):
    id = Col('id', show=False)
    title = Col('Title')
    course_code = Col('Code')
    view = LinkCol('View Course', 'course_detail', url_kwargs=dict(id='id'))

    




    