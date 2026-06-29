import matplotlib
matplotlib.use('Agg') # It was caused by Matplotlib using a GUI backend (Tkinter) inside a Flask threaded environment. I resolved it by switching Matplotlib to the Agg backend, which is non-GUI and suitable for server-side image generation.

import matplotlib.pyplot as plt

# def application_chart_funnel(funnel):
#     labels=["Waiting","Shortlisted","Rejected"]
#     values = [
#     funnel["Waiting"],
#     funnel["Shortlisted"],
#     funnel["Rejected"]]
#     plt.figure(figsize=(8,5))
#     plt.bar(labels,values)
#     plt.title("Application Funnel")
#     plt.ylabel("Number OF Applications")
#     plt.tight_layout()
#     plt.savefig("static/images/funnel.png")
#     plt.close()
# def top_companies_chart(top):
#     plt.figure(figsize=(8,5))
#     plt.barh(top.index,top.values)
#     plt.title("Top Hiring Companies")
#     plt.xlabel("Shortlisted Students")
#     plt.tight_layout()
#     plt.savefig("static/images/top_companies.png")
#     plt.close()
# def department_chart(department):
#     plt.figure(figsize=(8,5))
#     plt.barh(department.index,department.values)
#     plt.title("Department-Wise Applications")
#     plt.ylabel("Applications")
#     plt.tight_layout()
#     plt.savefig("static/images/department_chart.png")
#     plt.close()
# def average_salary_chart(avg_salary):
#     plt.figure(figsize=(8,5))
#     plt.bar(avg_salary.index,avg_salary.values)
#     plt.title(
#         "Average Salary by Company"
#     )

#     plt.ylabel(
#         "Salary"
#     )
#     plt.tight_layout()

#     plt.savefig(
#         "static/images/salary_chart.png"
#     )
#     plt.close()

# def highest_salary_chart(highest_salary):

#     plt.figure(figsize=(8,5))

#     plt.bar(
#         highest_salary.index,
#         highest_salary.values
#     )

#     plt.title(
#         "Highest Salary by Company"
#     )

#     plt.ylabel(
#         "Salary"
#     )

#     plt.tight_layout()

#     plt.savefig(
#         "static/images/highest_salary_chart.png"
#     )

#     plt.close()

# def job_role_chart(jobs):

#     plt.figure(figsize=(8,5))

#     plt.barh(
#         jobs.index,
#         jobs.values
#     )

#     plt.title(
#         "Job Role Popularity"
#     )

#     plt.xlabel(
#         "Number of Drives"
#     )

#     plt.tight_layout()

#     plt.savefig(
#         "static/images/job_role_chart.png"
#     )

#     plt.close()



# def monthly_trend_chart(monthly):

#     plt.figure(figsize=(8,5))

#     plt.plot(
#         monthly.index.astype(str),
#         monthly.values,
#         marker="o"
#     )

#     plt.title(
#         "Monthly Application Trend"
#     )

#     plt.xlabel(
#         "Month"
#     )

#     plt.ylabel(
#         "Applications"
#     )

#     plt.tight_layout()

#     plt.savefig(
#         "static/images/monthly_trend_chart.png"
#     )

#     plt.close()

