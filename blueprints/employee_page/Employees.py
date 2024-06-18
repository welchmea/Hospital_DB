from flask import Blueprint, render_template, request, redirect
import psycopg2
import os
# from ...config import load_config

emp_main = Blueprint('employee_page', __name__)


# def connect(config):
#     """ Connect to the PostgreSQL database server """
#     try:
#         # connecting to the PostgreSQL server
#         with psycopg2.connect(**config) as conn:
#             print('Connected to the PostgreSQL server.')
#             return conn
#     except (psycopg2.DatabaseError, Exception) as error:
#         print(error)
# config = load_config()
# conn = connect(config)

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')


# ---------------------------
# --- CRUD for Employees ----
# ---------------------------


# Route for employees page
@emp_main.route("/employees", methods=["POST", "GET"])
def employees():
    
    # Grabs employees data from mySQl and call template to display
    if request.method == "GET":
        # mySQL query to grab all from Departments
        query = "SELECT Employees.employeeID, Employees.name, \
        Employees.email, Employees.phoneNum, \
        EmploymentTypes.typeName, Jobs.jobName, \
        Departments.depName FROM Employees \
        LEFT JOIN Jobs ON Employees.jobID = Jobs.jobID  \
        LEFT JOIN Departments ON Employees.departmentID = Departments.departmentID \
        LEFT JOIN EmploymentTypes ON Employees.typeName = EmploymentTypes.typeName;"
        cur = conn.cursor()
        cur.execute(query)
        employees_data = cur.fetchall()

        return render_template("employees.j2", employees_data=employees_data)


# Route for delete functionality, deleting selected employee by employeeID
@emp_main.route("/delete_employees/<int:employeeid>")
def delete_employees(employeeid):
    # mySQL query to delete the employee with passed id
    query = "DELETE FROM Employees WHERE employeeid = '%s';"
    cur = conn.cursor()
    cur.execute(query, [employeeid])
    conn.commit()

    # Redirect back to employee page
    return redirect("/employees")


# Route for edit functionality, updating the attributes of an employee
# Passes the 'employeeID' value of selected department on button click via the route
@emp_main.route("/edit_employee/<int:employeeid>", methods=["POST", "GET"])
def edit_employee(employeeid):
    
    if request.method == "GET":
        # mySQL query to grab the info of the Employee with passed id
        query = "SELECT * FROM Employees WHERE employeeid = %s" % employeeid
        cur = conn.cursor()
        cur.execute(query)
        employees_data = cur.fetchall()
        query2 = "SELECT typename FROM EmploymentTypes"
        cur = conn.cursor()
        cur.execute(query2)
        emptypefk = cur.fetchall()
        query3 = "SELECT jobID, jobname FROM Jobs;"
        cur = conn.cursor()
        cur.execute(query3)
        jobidfk = cur.fetchall()
        query4 = "SELECT departmentID, depname FROM Departments"
        cur = conn.cursor()
        cur.execute(query4)
        departmentfk = cur.fetchall() 

        # Render edit_employee page passing query data to the edit_employee template
        return render_template("edit_employee.j2", employees_data=employees_data,
            emptypefk=emptypefk, jobidfk=jobidfk, departmentfk=departmentfk)

    # Conditional to alter table contents in database
    if request.method == "POST":
        # grab user form inputs
        if request.form.get('edit_employee'):
            employeeid = request.form["employeeid"]
            name = request.form["name"]
            email = request.form["email"]
            phonenum = request.form["phonenum"]
            typename = request.form["typename"]
            jobid = request.form["jobid"]
            departmentid = request.form["departmentid"] 

            # Account for null email and departmentID
            if departmentid == '0' and email == "":
                query = "UPDATE Employees SET name = %s, email = NULL, phonenum = %s, typename = %s, \
                jobid = %s, departmentid = NULL WHERE employeeid = %s"
                cur = conn.cursor()
                cur.execute(query, (name, phonenum, typename, jobid, employeeid))
                conn.commit()
                return redirect("/employees")

            # Account for null email
            if email == "":
                query = "UPDATE Employees SET name = %s, email = NULL, phonenum = %s, typename = %s, \
                jobid = %s, departmentid = %s WHERE employeeid = %s"
                cur = conn.cursor()
                cur.execute(query, (name, phonenum, typename, jobid, departmentid, employeeid))
                conn.commit()
                return redirect("/employees")

            # Account for null departmentID
            if departmentid == '0':
                query = "UPDATE Employees SET name = %s, email = %s, phonenum = %s, typename = %s, \
                jobid = %s, departmentid = NULL WHERE employeeid = %s"
                cur = conn.cursor()
                cur.execute(query, (name, email, phonenum, typename, jobid, employeeid))
                conn.commit()
                return redirect("/employees")

            # No null inputs
            else:
                query = "UPDATE Employees SET name = %s, email = %s, phoneNum = %s, typeName = %s, \
                jobid = %s, departmentid = %s WHERE employeeid = %s"
                cur = conn.cursor()
                cur.execute(query, (name, email, phonenum, typename, jobid, departmentid, employeeid))
                conn.commit()
                return redirect("/employees")


# Route for add functionality, adds new employee data
@emp_main.route("/add_employee", methods=["POST", "GET"])
def add_employee():
    
    # Inserts data about a new employee into the Employees entity
    if request.method == "POST":
        if request.form.get("add_employee"):
            # Grab user form inputs
            name = request.form["name"]
            email = request.form["email"]
            phonenum = request.form["phonenum"]
            typename = request.form["typename"]
            jobid = request.form["jobid"]
            departmentid = request.form["departmentid"] 

            # Account for null email and departmentID
            if departmentid is None and email is None:
                query = "INSERT INTO Employees (name, phoneNum, typeName, jobID ) \
                VALUES (%s, %s,\
                    (SELECT typeName FROM EmploymentTypes WHERE typeName=%s),\
                    (SELECT jobID FROM Jobs WHERE jobName = %s));"
                cur = conn.cursor()
                cur.execute(query, (name, phonenum, typename, jobid))
                conn.commit()

            # Account for null email
            elif email is None:
                query = "INSERT INTO Employees (name, phoneNum, typeName, jobID, departmentID) \
                VALUES (%s, %s,\
                    (SELECT typeName FROM EmploymentTypes WHERE typeName=%s), \
                    (SELECT jobID FROM Jobs WHERE jobName = %s),\
                    (SELECT departmentID FROM Departments WHERE depName = %s));"
                cur = conn.cursor()
                cur.execute(query, (name, phonenum, typename, jobid, departmentid))
                conn.commit()

            # Account for null departmentID
            elif departmentid is None:
                query = "INSERT INTO Employees (name, email, phoneNum, typeName, jobID) \
                VALUES ( %s, %s, %s, \
                    (SELECT typeName FROM EmploymentTypes WHERE typeName=%s),\
                    (SELECT jobID FROM Jobs WHERE jobName = %s));"
                cur = conn.cursor()
                cur.execute(query, (name, email, phonenum, typename, jobid))
                conn.commit()

            # No null inputs
            else:
                query = "INSERT INTO Employees (name, email, phoneNum, typeName, jobID, departmentID) \
                VALUES (%s, %s, %s, \
                    (SELECT typeName FROM EmploymentTypes WHERE typeName=%s), \
                    (SELECT jobID FROM Jobs WHERE jobName = %s),\
                    (SELECT departmentID FROM Departments WHERE depName = %s));"
                cur = conn.cursor()
                cur.execute(query, (name, email, phonenum, typename, jobid, departmentid))
                conn.commit()

        # Redirect back to departments page after executing the add query
        return redirect("/employees")

    # Button click will render a new page so the user can add a new Employee
    if request.method == "GET":
        query = "SELECT * FROM Employees"
        cur = conn.cursor()
        cur.execute(query)
        employees_data = cur.fetchall()
        query2 = "SELECT typeName FROM EmploymentTypes"
        cur = conn.cursor()
        cur.execute(query2)
        emptypefk = cur.fetchall()
        query3 = "SELECT jobID, jobName FROM Jobs;"
        cur = conn.cursor()
        cur.execute(query3)
        jobidfk = cur.fetchall()
        query4 = "SELECT departmentID, depName FROM Departments"
        cur = conn.cursor()
        cur.execute(query4)
        departmentfk = cur.fetchall() 
        return render_template("add_employee.j2", 
                               employees_data=employees_data,
                               emptypefk=emptypefk, jobidfk=jobidfk, 
                               departmentfk=departmentfk)
