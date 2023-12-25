from flask import Blueprint, render_template, redirect, request
import psycopg2


dept_emp = Blueprint('deptEmp_page', __name__)

# -------------------------------------------
# - CRD for Department has EmploymentTypes -
# -------------------------------------------


def get_connection():
    conn = psycopg2.connect(host='ec2-3-232-218-211.compute-1.amazonaws.com', database='d6af5e5pibqrf1', user='xbeltbfqliosyk', password='294e9b67571b4e7e9ed12a10d8f0a5591750f681382b0a8193eeece39e5fde68')
    return conn

conn = get_connection()


@dept_emp.route("/dep_empTypes", methods=["GET"])
def dep_empTypes():
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
        dep_empTypes_data = cur.fetchall()

    return render_template("dep_empTypes.j2", dep_empTypes_data=dep_empTypes_data)

# Route for delete functionality, deleting selected Department EmploymentType by empDeptID
@dept_emp.route("/delete_dep_empTypes/<int:empDeptID>")
def delete_dep_empTypes(empDeptID):
    # mySQL query to delete the schedule with passed id
    query = "DELETE FROM Department_has_EmploymentTypes WHERE empDeptID = '%s';"
    cur = conn.cursor()
    cur.execute(query, [empDeptID])
    conn.commit()

    # Redirect back to schedules page
    return redirect("/dep_empTypes")

# Route for add functionality, adds the attributes of a department employmentType
@dept_emp.route("/add_dep_empTypes", methods=["POST", "GET"])
def add_dep_empTypes():
    # Inserts data about a new schedule into the schedules entity
    if request.method == "POST":
        # grab user form inputs
        if request.form.get("add_dep_empTypes"):
            typeName = request.form["typeName"]             # FK
            departmentID = request.form["departmentID"]     # FK

        # Account for null typeName
        if typeName is None:
            query = "INSERT INTO Department_has_EmploymentTypes (departmentID) \
             VALUES((SELECT departmentID FROM Departments WHERE depName = %s));"
            cur = conn.cursor()
            cur.execute(query, (departmentID))
            conn.commit()

        # Account for null departmentID
        if departmentID is None:
            query = "INSERT INTO Department_has_EmploymentTypes (typeName) \
            VALUES((SELECT typeName FROM EmploymentTypes WHERE typeName = %s));"
            cur = conn.cursor()
            cur.execute(query, (typeName))
            conn.commit()

        # No null inputs
        else:
            query = "INSERT INTO Department_has_EmploymentTypes (departmentID, typeName) \
            VALUES((SELECT departmentID FROM Departments WHERE depName = %s),\
            (SELECT typeName FROM EmploymentTypes WHERE typeName = %s));"
            cur = conn.cursor()
            cur.execute(query, (departmentID, typeName))
            conn.commit()

        # Redirect back to Department Has EmploymentTypes page after executing the add query
        return redirect("/dep_empTypes")

    # Button click renders new page to add EmpType/Department Data
    if request.method == "GET":
        query = "SELECT * FROM Department_has_EmploymentTypes"
        cur = conn.cursor()
        cur.execute(query)
        dep_empTypes_data = cur.fetchall()
        query2 = "SELECT departmentID, depName FROM Departments"
        cur = conn.cursor()
        cur.execute(query2)
        departmentFK = cur.fetchall()
        query3 = "SELECT typeName FROM EmploymentTypes"
        cur = conn.cursor()
        cur.execute(query3)
        empTypeFK = cur.fetchall()
        return render_template("add_dep_empTypes.j2",
                               dep_empTypes_data=dep_empTypes_data,
                               departmentFK=departmentFK,
                               empTypeFK=empTypeFK)