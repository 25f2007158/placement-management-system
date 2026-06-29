import pandas as pd
from applications.models import Student,Drive,Application,Companies
from applications.database import db

def load_data():
    students=pd.read_sql(Student.query.statement,db.engine)
    drive=pd.read_sql(Drive.query.statement,db.engine)
    applications=pd.read_sql(Application.query.statement,db.engine)
    companies=pd.read_sql(Companies.query.statement,db.engine)

    return students,drive,applications,companies
