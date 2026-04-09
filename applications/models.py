from .database import db #context of the application is the root directotry
#no dot:looks in root directory(in my project :MAD-1) 
# with dot: looks in currect directiory  
# from application.database : the models.py will think that there is 1 more same folder 

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(),nullable=False,unique=True)
    email=db.Column(db.String(),nullable=False,unique=True)
    password=db.Column(db.String(),nullable=False)
    role=db.Column(db.String())
class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    name = db.Column(db.String(150), nullable=False)
    department = db.Column(db.String(100),nullable=False)
    skills = db.Column(db.String(100),nullable=False)
    projects= db.Column(db.String(100),nullable=False)
    experience= db.Column(db.String(100),nullable=False)
    applications = db.relationship('Application', backref='student', lazy=True)
class Companies(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name=db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(20), default="pending")
    description=db.Column(db.String(150), nullable=False,default="We are excited to offer you an opportunity to be a part of our organization. Explore the role, review the requirements, and apply if your skills and interests align with what we’re looking for.")
    drives = db.relationship('Drive', backref='companies', lazy=True)
class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    drive_name=db.Column(db.String(150), nullable=False)
    job_title=db.Column(db.String(150), nullable=False)
    job_description=db.Column(db.String(150), nullable=False)
    salary=db.Column(db.Integer,nullable=False)
    location=db.Column(db.String(150), nullable=False)
    
    eligibility=db.Column(db.String(150), nullable=False)
    deadline = db.Column(db.Date)
    status = db.Column(db.String(20), default='upcoming')
    
    applications = db.relationship('Application', backref='drive', lazy=True)
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'))
    status = db.Column(db.String(20),nullable=False)  
    applied_at = db.Column(db.Date,nullable=False)
    
    

    

    




                     