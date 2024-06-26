from flask import Blueprint, render_template, redirect, request
import psycopg2
import os 
# from ...config import load_config

dept_emp = Blueprint('deptEmp_page', __name__)

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


# -------------------------------------------
# - CRD for Department has EmploymentTypes -
# -------------------------------------------


@dept_emp.route("/dep_emptypes", methods=["GET"])
def dep_emptypes():
    
    # Grabs Department has EmploymentTypes data from mySQl and call template to display
    if request.method == "GET":
        # mySQL query to grab all from Department has EmploymentTypes data
        query = "SELECT Department_has_EmploymentTypes.empdeptid,\
            EmploymentTypes.typename, \
            Departments.depName \
            FROM Department_has_EmploymentTypes \
            LEFT JOIN EmploymentTypes \
            ON EmploymentTypes.typename = Department_has_EmploymentTypes.typename \
            LEFT JOIN Departments \
            ON Departments.departmentid = Department_has_EmploymentTypes.departmentid;"
        cur = conn.cursor()
        cur.execute(query)
        dep_emptypes_data = cur.fetchall()

        return render_template("dep_emptypes.j2", dep_emptypes_data=dep_emptypes_data)


# Route for delete functionality, deleting selected Department EmploymentType by empdeptid
@dept_emp.route("/delete_dep_emptypes/<int:empdeptid>")
def delete_dep_emptypes(empdeptid):
    # mySQL query to delete the schedule with passed id
    query = "DELETE FROM Department_has_EmploymentTypes WHERE empdeptid = '%s';"
    cur = conn.cursor()
    cur.execute(query, [empdeptid])
    conn.commit()

    # Redirect back to schedules page
    return redirect("/dep_emptypes")


# Route for add functionality, adds the attributes of a department employmentType
@dept_emp.route("/add_dep_emptypes", methods=["POST", "GET"])
def add_dep_emptypes():
    
    # Inserts data about a new schedule into the schedules entity
    if request.method == "POST":
        # grab user form inputs
        if request.form.get("add_dep_emptypes"):
            typename = request.form["typename"]             # FK
            departmentid = request.form["departmentid"]     # FK

            # Account for null typename
            if typename is None:
                query = "INSERT INTO Department_has_EmploymentTypes (departmentid) \
                VALUES((SELECT departmentid FROM Departments WHERE depName = %s));"
                cur = conn.cursor()
                cur.execute(query, departmentid)
                conn.commit()

            # Account for null departmentid
            if departmentid is None:
                query = "INSERT INTO Department_has_EmploymentTypes (typename) \
                VALUES((SELECT typename FROM EmploymentTypes WHERE typename = %s));"
                cur = conn.cursor()
                cur.execute(query, typename)
                conn.commit()

            # No null inputs
            else:
                query = "INSERT INTO Department_has_EmploymentTypes (departmentid, typename) \
                VALUES((SELECT departmentid FROM Departments WHERE depName = %s),\
                (SELECT typename FROM EmploymentTypes WHERE typename = %s));"
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
        query2 = "SELECT departmentid, depName FROM Departments"
        cur = conn.cursor()
        cur.execute(query2)
        departmentfk = cur.fetchall()
        query3 = "SELECT typename FROM EmploymentTypes"
        cur = conn.cursor()
        cur.execute(query3)
        emptypefk = cur.fetchall()
        return render_template("add_dep_emptypes.j2",
                               dep_emptypes_data=dep_emptypes_data,
                               departmentfk=departmentfk,
                               emptypefk=emptypefk)
