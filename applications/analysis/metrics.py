import pandas as pd

def application_funnel(applications):  #APPLICATION FUNNEL
    applications["status"] = applications["status"].str.lower()
    funnel=applications["status"].value_counts()
    return {
        "Total Applications": int(funnel.sum()),
        "Waiting": int(funnel.get("pending", 0)),
        "Shortlisted": int(funnel.get("shortlisted", 0)),  
        "Rejected": int(funnel.get("rejected", 0))
    }

def top_companies(drive,applications,companies): #TOP COMPANIES 
    shortlisted=applications[applications["status"]=="shortlisted"]
    merge1=shortlisted.merge(drive,left_on="drive_id",right_on="id")
    merged=merge1.merge(companies,left_on="company_id",right_on="id")

    return merged["name"].value_counts().head(5)
#
def department_wise_applications(student,applications):#DEPARTMENT-WISE APPLICATION 
    d_W_A=student.merge(applications,left_on="id",right_on="student_id")
    return d_W_A["department"].value_counts()
#
def avg_salary_by_company(drive,companies): #AVG SALARY BY COMPANY 
    merge=companies.merge(drive,left_on="id",right_on="company_id")
    return {"Average Package":merge.groupby("name")["salary"].mean().sort_values(ascending=False),
            "Highest Package":merge.groupby("name")["salary"].max().sort_values(ascending=False)}
#
def job_title(drive): #JOB POPULARITY
    return drive["job_title"].value_counts().head(10)
#
def monthly_application_trend(application): 
    application["applied_at"]=pd.to_datetime(application["applied_at"])
    application["month"]=(application["applied_at"].dt.to_period("M"))
    return application.groupby("month").size()  
