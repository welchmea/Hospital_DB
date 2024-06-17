# All blueprints folder .py files were adapted from source code
# CS 340 flask-starter-app
from flask import Flask
from .blueprints.department_page.Departments import emp_department
from .blueprints.jobDept.Jobs_has_Departments import jobdepartment
from .blueprints.main_page.index import index_page
from .blueprints.deptEmp_page.Department_has_EmploymentTypes import dept_emp
from .blueprints.schedule_page.Schedules import emp_schedule
from .blueprints.employee_page.Employees import emp_main
from .blueprints.job_page.Jobs import emp_job
from .blueprints.empTypes.EmploymentTypes import employType

app = Flask(__name__)

# creates routes to code of entity CRUD operations in blueprints folder
app.register_blueprint(index_page)
app.register_blueprint(jobdepartment)
app.register_blueprint(dept_emp)
app.register_blueprint(emp_schedule)
app.register_blueprint(emp_job)
app.register_blueprint(emp_department)
app.register_blueprint(emp_main)
app.register_blueprint(employType)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
