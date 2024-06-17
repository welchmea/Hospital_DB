from flask import Blueprint, render_template, redirect, request
import psycopg2
import os 
from ...config import load_config

dept_emp = Blueprint('deptEmp_page', __name__)

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


# DATABASE_URL = os.environ['DATABASE_URL']

# conn = psycopg2.connect(DATABASE_URL, sslmode='require')

config = load_config()
conn = connect(config)
# -------------------------------------------
# - CRD for Department has EmploymentTypes -
# -------------------------------------------


@dept_emp.route("/dep_emptypes", methods=["GET"])
def dep_emptypes():
    
    dep_emptypes_data = None
    # Grabs Department has EmploymentTypes data from mySQl and call template to display
    if request.method == "GET":
        # mySQL query to grab all from Department has EmploymentTypes data
        query = "SELECT Department_has_EmploymentTypes.empDeptID,\
            EmploymentTypes.typeName, \
            Departments.depName \
            FROM Department_has_EmploymentTypes \
            LEFT JOIN EmploymentTypes \
            ON EmploymentTypes.typeName = Department_has_EmploymentTypes.typeName \
            LEFT JOIN Departments \
            ON Departments.departmentID = Department_has_EmploymentTypes.departmentID;"
        cur = conn.cursor()
        cur.execute(query)
        dep_emptypes_data = cur.fetchall()

    return render_template("dep_emptypes.j2", dep_emptypes_data=dep_emptypes_data)


# Route for delete functionality, deleting selected Department EmploymentType by empDeptID
@dept_emp.route("/delete_dep_emptypes/<int:empDeptID>")
def delete_dep_emptypes(empdeptid):
    # mySQL query to delete the schedule with passed id
    query = "DELETE FROM Department_has_EmploymentTypes WHERE empDeptID = '%s';"
    cur = conn.cursor()
    cur.execute(query, [empdeptid])
    conn.commit()

    # Redirect back to schedules page
    return redirect("/dep_emptypes")


# Route for add functionality, adds the attributes of a department employmentType
@dept_emp.route("/add_dep_emptypes", methods=["POST", "GET"])
def add_dep_emptypes():
    
    typename, departmentid, dep_emptypes_data = None, None, None
    # Inserts data about a new schedule into the schedules entity
    if request.method == "POST":
        # grab user form inputs
        if request.form.get("add_dep_empTypes"):
            typename = request.form["typeName"]             # FK
            departmentid = request.form["departmentID"]     # FK

        # Account for null typeName
        if typename is None:
            query = "INSERT INTO Department_has_EmploymentTypes (departmentID) \
             VALUES((SELECT departmentID FROM Departments WHERE depName = %s));"
            cur = conn.cursor()
            cur.execute(query, departmentid)
            conn.commit()

        # Account for null departmentID
        if departmentid is None:
            query = "INSERT INTO Department_has_EmploymentTypes (typeName) \
            VALUES((SELECT typeName FROM EmploymentTypes WHERE typeName = %s));"
            cur = conn.cursor()
            cur.execute(query, typename)
            conn.commit()

        # No null inputs
        else:
            query = "INSERT INTO Department_has_EmploymentTypes (departmentID, typeName) \
            VALUES((SELECT departmentID FROM Departments WHERE depName = %s),\
            (SELECT typeName FROM EmploymentTypes WHERE typeName = %s));"
            cur = conn.cursor()
            cur.execute(query, (departmentid, typename))
            conn.commit()

        # Redirect back to Department Has EmploymentTypes page after executing the add query
        return redirect("/dep_emptypes")

    # Button click renders new page to add EmpType/Department Data
    if request.method == "GET":
        query = "SELECT * FROM Department_has_EmploymentTypes"
        cur = conn.cursor()
        cur.execute(query)
        dep_emptypes_data = cur.fetchall()
        query2 = "SELECT departmentID, depName FROM Departments"
        cur = conn.cursor()
        cur.execute(query2)
        departmentfk = cur.fetchall()
        query3 = "SELECT typeName FROM EmploymentTypes"
        cur = conn.cursor()
        cur.execute(query3)
        emptypefk = cur.fetchall()
        return render_template("add_dep_emptypes.j2",
                               dep_emptypes_data=dep_emptypes_data,
                               departmentfk=departmentfk,
                               emptypefk=emptypefk)
