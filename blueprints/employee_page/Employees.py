from flask import Blueprint, render_template, request, redirect
import psycopg2
import os
# from config import load_config

emp_main = Blueprint('employee_page', __name__)


# -----------------------------
# --- CRUD for Departments ----
# -----------------------------
# def connect(config):
#     """ Connect to the PostgreSQL database server """
#     try:
#         # connecting to the PostgreSQL server
#         with psycopg2.connect(**config) as conn:
#             print('Connected to the PostgreSQL server.')
#             return conn
#     except (psycopg2.DatabaseError, Exception) as error:
#         print(error)
        
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# config = load_config()
# conn = connect(config)
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
@emp_main.route("/delete_employees/<int:employeeID>")
def delete_employees(employeeID):
    # mySQL query to delete the employee with passed id
    query = "DELETE FROM Employees WHERE employeeID = '%s';"
    cur = conn.cursor()
    cur.execute(query, [employeeID])
    conn.commit()

    # Redirect back to employee page
    return redirect("/employees")

# Route for edit functionality, updating the attributes of an employee
# Passes the 'employeeID' value of selected department on button click via the route
@emp_main.route("/edit_employee/<int:employeeID>", methods=["POST", "GET"])
def edit_employee(employeeID):
    if request.method == "GET":
        # mySQL query to grab the info of the Employee with passed id
        query = "SELECT * FROM Employees WHERE employeeID = %s" % (employeeID)
        cur = conn.cursor()
        cur.execute(query)
        employees_data = cur.fetchall()
        query2 = "SELECT typeName FROM EmploymentTypes"
        cur = conn.cursor()
        cur.execute(query2)
        empTypeFK = cur.fetchall()
        query3 = "SELECT jobID, jobName FROM Jobs;"
        cur = conn.cursor()
        cur.execute(query3)
        jobIDFK = cur.fetchall()
        query4 = "SELECT departmentID, depName FROM Departments"
        cur = conn.cursor()
        cur.execute(query4)
        departmentFK = cur.fetchall() 

        # Render edit_employee page passing query data to the edit_employee template
        return render_template("edit_employee.j2", employees_data=employees_data, empTypeFK=empTypeFK, jobIDFK=jobIDFK, departmentFK=departmentFK )

    # Conditional to alter table contents in database
    if request.method == "POST":
        # grab user form inputs
        if request.form.get('edit_employee'):
            employeeID = request.form["employeeID"]
            name = request.form["name"]
            email = request.form["email"]
            phoneNum = request.form["phoneNum"]
            typeName = request.form["typeName"]
            jobID = request.form["jobID"]
            departmentID = request.form["departmentID"] 

        # Account for null email and departmentID
        if departmentID == '0' and email == "":
            query = "UPDATE Employees SET name = %s, email = NULL, phoneNum = %s, typeName = %s, \
            jobID = %s, departmentID = NULL WHERE employeeID = %s"
            cur = conn.cursor()
            cur.execute(query, (name, phoneNum, typeName, jobID, employeeID))
            conn.commit()
            return redirect("/employees")

        # Account for null email
        if email == "":
            query = "UPDATE Employees SET name = %s, email = NULL, phoneNum = %s, typeName = %s, \
            jobID = %s, departmentID = %s WHERE employeeID = %s"
            cur = conn.cursor()
            cur.execute(query, (name, phoneNum, typeName, jobID, departmentID, employeeID))
            conn.commit()
            return redirect("/employees")

        # Account for null departmentID
        if departmentID == '0':
            query = "UPDATE Employees SET name = %s, email = %s, phoneNum = %s, typeName = %s, \
            jobID = %s, departmentID = NULL WHERE employeeID = %s"
            cur = conn.cursor()
            cur.execute(query, (name, email, phoneNum, typeName, jobID, employeeID))
            conn.commit()
            return redirect("/employees")

        # No null inputs
        else:
            query = "UPDATE Employees SET name = %s, email = %s, phoneNum = %s, typeName = %s, \
            jobID = %s, departmentID = %s WHERE employeeID = %s"
            cur = conn.cursor()
            cur.execute(query, (name, email, phoneNum, typeName, jobID, departmentID, employeeID))
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
            phoneNum = request.form["phoneNum"]
            typeName = request.form["typeName"]
            jobID = request.form["jobID"]
            departmentID = request.form["departmentID"] 

        # Account for null email and departmentID
        if departmentID == None and email == None:
            query = "INSERT INTO Employees (name, phoneNum, typeName, jobID ) \
            VALUES (%s, %s,\
                (SELECT typeName FROM EmploymentTypes WHERE typeName=%s),\
                (SELECT jobID FROM Jobs WHERE jobName = %s));"
            cur = conn.cursor()
            cur.execute(query, (name, phoneNum, typeName, jobID))
            conn.commit()

        # Account for null email
        elif email == None:
            query = "INSERT INTO Employees (name, phoneNum, typeName, jobID, departmentID) \
            VALUES (%s, %s,\
                (SELECT typeName FROM EmploymentTypes WHERE typeName=%s), \
                (SELECT jobID FROM Jobs WHERE jobName = %s),\
                (SELECT departmentID FROM Departments WHERE depName = %s));"
            cur = conn.cursor()
            cur.execute(query, (name, phoneNum, typeName, jobID, departmentID))
            conn.commit()

        # Account for null departmentID
        elif departmentID == None:
            query = "INSERT INTO Employees (name, email, phoneNum, typeName, jobID) \
            VALUES ( %s, %s, %s, \
                (SELECT typeName FROM EmploymentTypes WHERE typeName=%s),\
                (SELECT jobID FROM Jobs WHERE jobName = %s));"
            cur = conn.cursor()
            cur.execute(query, (name, email, phoneNum, typeName, jobID))
            conn.commit()

        # No null inputs
        else:
            query = "INSERT INTO Employees (name, email, phoneNum, typeName, jobID, departmentID) \
            VALUES (%s, %s, %s, \
                (SELECT typeName FROM EmploymentTypes WHERE typeName=%s), \
                (SELECT jobID FROM Jobs WHERE jobName = %s),\
                (SELECT departmentID FROM Departments WHERE depName = %s));"
            cur = conn.cursor()
            cur.execute(query, (name, email, phoneNum, typeName, jobID, departmentID))
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
        empTypeFK = cur.fetchall()
        query3 = "SELECT jobID, jobName FROM Jobs;"
        cur = conn.cursor()
        cur.execute(query3)
        jobIDFK = cur.fetchall()
        query4 = "SELECT departmentID, depName FROM Departments"
        cur = conn.cursor()
        cur.execute(query4)
        departmentFK = cur.fetchall() 
        return render_template("add_employee.j2", 
                               employees_data=employees_data, \
                               empTypeFK=empTypeFK, jobIDFK=jobIDFK, 
                               departmentFK=departmentFK)