#this file is only used to write routes
from flask import Flask,render_template,request,redirect,session
from flask import current_app as app  #will not show circular import error 
from .models import *
from datetime import datetime
from applications.analysis.data_loader import load_data
from applications.analysis.metrics import * 
from applications.analysis.charts import *
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        # password=request.form['password'] here if the value is not given then it will show error
        # password=request.form.get('password') here if the value is not given then it will not show error
        username = request.form.get("username") 
        password = request.form.get("password")
        
        this_user=User.query.filter_by(username=username).first()#the first row where the username matches the username extracted 
        if this_user:
            print("ROLE FROM DB:", this_user.role)
            if this_user.password==password: #write . to access the data of table
                session["user_id"]=this_user.id
                session["role"] = this_user.role
                if this_user.role=="student":
                    return redirect("/student")
                elif this_user.role=="company":
                    return redirect("/company")
                elif this_user.role == "admin":
                     return redirect('/admin')
                else:
                    return "Invalid role"
            else:
                return render_template("incoorect_password.html")
        else:
            return render_template("register.html")
    return render_template("login.html") #because GET is used to show form
@app.route('/register',methods=["GET","POST"])
def register():
    if request.method=='POST':
        username=request.form.get("username") 
        email=request.form.get("email")
        password=request.form.get("password")
        role = request.form.get("role")
        if role not in ["student", "company"]:
            return "Invalid role"
        user_name=User.query.filter_by(username=username).first()
        user_email=User.query.filter_by(email=email).first()
        if user_name or user_email:
            return render_template("already.html")
        else:
            new_user=User(username=username,email=email,password=password,role=role)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/login")
        
    return render_template("register.html")
@app.route('/admin')
def admim_dashboard():
    if session.get("role") != "admin":
        return "Unauthorized"
    approved_companies = Companies.query.filter_by(status="approved").all()
    pending_companies = Companies.query.filter_by(status="pending").all()
    blacklisted_companies = Companies.query.filter_by(status="blacklisted").all()
    students = Student.query.all()  
    ongoing_drives = Drive.query.filter_by(status="open").all()
    applications = Application.query.all()
    
    return render_template(
        "admin_dashboard.html",
        approved_companies=approved_companies,
        pending_companies=pending_companies,
        blacklisted_companies=blacklisted_companies,
        students=students,
        ongoing_drives=ongoing_drives,
        applications=applications
    )
@app.route("/company")
def company_dashboard():
    
    company = Companies.query.filter_by(user_id=session.get("user_id")).first()
    if not company:
        return redirect("/create_company_profile")
    active_drives = Drive.query.filter(
    Drive.company_id == company.id, 
    Drive.status.in_(['open', 'upcoming'])
).all()
    closed_drives=Drive.query.filter_by(company_id=company.id,status="closed").all()

    return render_template("company_dashboard.html", company=company,closed_drives=closed_drives,upcoming_drives=active_drives)
@app.route("/student")
def student_dashboard():
    user_id=session.get("user_id")
    if not user_id:
        return redirect("/login")
    student=Student.query.filter_by(user_id=user_id).first()
    if not student:
        return redirect("/create_profile")
    companies = Companies.query.join(Drive).filter(Companies.status=="approved",Drive.status=="open").all() #important
    
    applications = Application.query.filter_by(student_id=student.id).all()
    
    return render_template("student_dashboard.html", student=student,companies=companies,applications=applications)

@app.route("/create_drive", methods=["GET", "POST"])
def create_drive():
    if session.get("role") != "company":
        return "Unauthorized"

    user_id = session.get("user_id")
    company = Companies.query.filter_by(user_id=user_id).first()
    if company.status=="blacklisted":
        return "Your Company is blacklisted,Hence you cannot create drive"
    
    if request.method == "POST":

        drive_name = request.form.get("drive_name")
        job_title = request.form.get("job_title")
        job_description = request.form.get("job_description")
        salary = request.form.get("salary")
        location = request.form.get("location")
        eligibility = request.form.get("eligibility")
        deadline = request.form.get("deadline")
        selected_status = request.form.get("status")
        if deadline:
            actual_date = datetime.strptime(deadline, '%Y-%m-%d').date()
        else:
            actual_date = None # Or handle as required

        new_drive = Drive(
            company_id=company.id,
            drive_name=drive_name,
            job_title=job_title,
            job_description=job_description,
            salary=salary,
            location=location,
            eligibility=eligibility,
            status=selected_status,
            deadline=actual_date,   
        )
        db.session.add(new_drive)
        db.session.commit()
        return redirect("/company")
    return render_template("create_drive.html")

@app.route("/applying_to_drive/<int:drive_id>",methods=["POST"])
def apply(drive_id):
    if session.get("role") != "student":
        return "Unauthorized"
    user_id=session.get("user_id")
    student = Student.query.filter_by(user_id=user_id).first()
    existing = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive_id).first()
    if existing:
        return redirect("/student")
    new_application = Application(
        student_id=student.id,
        drive_id=drive_id,
        status="pending",
        applied_at=datetime.today()
    )
    db.session.add(new_application)
    db.session.commit()
    return redirect("/student")

@app.route("/company_details/<int:id>")
def company_details(id):
    company=Companies.query.get(id)
    active_drives = Drive.query.filter(
    Drive.company_id == company.id, 
    Drive.status.in_(['open', 'upcoming'])
).all()
    return render_template(
        "company_details.html",
        company=company,
        drive=active_drives
    )
@app.route("/view_applications/<int:id>")
def view_applications(id):
    if session.get("role") != "company":
        return "Unauthorized"
    applications=Application.query.filter_by(drive_id=id).all()
    

    drive = Drive.query.get(id)

    return render_template(
    "view_application.html",
    applications=applications,
    drive=drive
)
@app.route("/update_application/<int:id>", methods=["POST"])
def update_application(id):
    if session.get("role") != "company":
        return "Unauthorized"
    app_object=Application.query.get(id)
    drive = Drive.query.get(app_object.drive_id)
    app_object.status=request.form.get("status")
    db.session.commit()
    return redirect(f"/view_applications/{drive.id}") #important 

@app.route("/close_drive/<int:id>", methods=["POST"])
def close_drive(id):
    drive = Drive.query.get(id)
    if not drive:
        return "Not Found"
    company = Companies.query.filter_by(user_id=session.get("user_id")).first()
    if drive.company_id != company.id:
        return "Unauthorized", 403
    drive.status = "closed"
    db.session.commit()

    return redirect("/company")

@app.route("/approve_company/<int:id>",methods=["POST"])
def approve_company(id):
    if session.get("role") != "admin":
        return "Unauthorized"
    company=Companies.query.get(id)
    if company:
        company.status="approved"
        db.session.commit()
    return redirect("/admin")

@app.route("/blacklist_company/<int:id>", methods=["POST"])
def blacklist_company(id):
    if session.get("role") != "admin":
        return "Unauthorized"
    company = Companies.query.get(id)
    if company:
        company.status = "blacklisted"
        db.session.commit()
    return redirect("/admin")

@app.route("/admin_close_drive/<int:id>", methods=["POST"])
def admin_close_drive(id):
    if session.get("role") != "admin":
        return "Unauthorized", 403
    drive = Drive.query.get(id)
    if drive:
        drive.status = "closed"
        db.session.commit()
    return redirect("/admin")

@app.route("/create_profile", methods=["GET", "POST"])
def create_profile():

    user_id = session.get("user_id")

    if request.method == "POST":

        name = request.form.get("name")
        department = request.form.get("department")
        skills = request.form.get("skills")
        projects = request.form.get("projects")
        experience = request.form.get("experience")

        new_student = Student(
            user_id=user_id,
            name=name,
            department=department,
            skills=skills,
            projects=projects,
            experience=experience
        )

        db.session.add(new_student)
        db.session.commit()

        return redirect("/student")

    return render_template("create_profile.html")

@app.route("/view_single_application/<int:id>")
def view_single_application(id):
    role = session.get("role")
    if role not in ["admin", "company"]:
        return "Unauthorized"
    
    # Get the specific application by its unique ID
    application = Application.query.get(id)
    if not application:
        return "Application Not Found"
        
    return render_template("application_details.html", application=application)

@app.route("/student_application_history")
def student_history():
    user_id = session.get("user_id")
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return redirect("/create_profile")
        
    
    applications = Application.query.filter_by(student_id=student.id).all()
    return render_template("student_application_history.html", applications=applications,student=student)

@app.route("/drive_details/<int:id>")
def drive_details(id):

    drive = Drive.query.get(id)
    if not drive:
        return "Drive not found"
    company = drive.companies
    open_drives = Drive.query.filter_by(company_id=company.id, status="open").all()
    return render_template("drive_details.html", drive=drive,open_drives=open_drives,company=company)

@app.route("/review_application/<int:app_id>")
def review_application(app_id):
    
    app_entry = Application.query.get(app_id)
    
    
    return render_template("student_application_approval.html", app=app_entry)     

@app.route("/apply_to_drive/<int:drive_id>")
def apply_to_drive(drive_id):

    if session.get("role") != "student":
        return "Only students can apply to drives"

    drive = Drive.query.get_or_404(drive_id)
    company = drive.companies
    open_drives = Drive.query.filter_by(company_id=company.id, status="open").all()
    

    return render_template("applying_to_drive.html",drive=drive,company=company,open_drives=open_drives) 
        
@app.route("/create_company_profile", methods=["GET", "POST"])
def create_company_profile():
    u_id = session.get("user_id")
    if not u_id:
        return redirect("/login")
    existing_company = Companies.query.filter_by(user_id=u_id).first()
    if existing_company:
        return redirect("/company_dashboard")

    if request.method == "POST":
        
        name = request.form.get("name")
        description = request.form.get("description")
        new_company = Companies(
            user_id=u_id,
            name=name,
            description=description 
        )     
        db.session.add(new_company)
        db.session.commit()
        return redirect("/company")

    return render_template("create_company_profile.html")
@app.route("/analytics")
def analytics():
    students, drives, applications, companies = load_data()
    funnel = application_funnel(applications)
    top = top_companies(
        drives,
        applications,
        companies
    )
    department = department_wise_applications(
        students,
        applications
    )
    salary = avg_salary_by_company(
        drives,
        companies
    )
    jobs = job_title(
        drives
    )
    monthly = monthly_application_trend(
        applications
    )
    return str(monthly)
