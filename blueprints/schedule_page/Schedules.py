from flask import Blueprint, render_template, request, redirect
import psycopg2
import os
# from ...config import load_config

emp_schedule = Blueprint('schedule_page', __name__)

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
# --- CRUD for Schedules ----
# ---------------------------


# Route for schedules page
@emp_schedule.route("/schedules", methods=["GET"])
def schedules():
    
    # Grabs schedules data from mySQl and call template to display
    if request.method == "GET":
        # mySQL query to grab all from Schedules
        query = "SELECT Schedules.scheduleID, \
            Schedules.scheduleType, \
            Schedules.shift, Schedules.startTime, \
            Schedules.endTime, \
            Employees.name, \
            EmploymentTypes.typeName, \
            Departments.depName \
            FROM Schedules LEFT JOIN Employees ON \
            Employees.employeeID = Schedules.employeeID \
            LEFT JOIN EmploymentTypes ON \
            EmploymentTypes.typeName = Schedules.typeName \
            LEFT JOIN Departments ON \
            Departments.departmentID = Schedules.departmentID;"
        cur = conn.cursor()
        cur.execute(query)
        schedules_data = cur.fetchall()

        return render_template("schedules.j2", schedules_data=schedules_data)


# Route for delete functionality, deleting selected schedule by scheduleID
@emp_schedule.route("/delete_schedules/<int:scheduleid>")
def delete_schedules(scheduleid):
    # mySQL query to delete the schedule with passed id
    query = "DELETE FROM Schedules WHERE scheduleID = '%s';"
    cur = conn.cursor()
    cur.execute(query, (scheduleid,))
    conn.commit()

    # Redirect back to schedules page
    return redirect("/schedules")


# Route for add functionality, adds new schedule data
@emp_schedule.route("/add_schedule", methods=["POST", "GET"])
def add_schedule():
    
    # Inserts data about a new schedule into the schedules entity
    if request.method == "POST":
        # grab user form inputs
        if request.form.get("add_schedule"):
            scheduletype = request.form["scheduletype"]     # NOT NULL
            shift = request.form["shift"]                   # NOT NULL
            starttime = request.form["starttime"]           # NOT NULL
            endtime = request.form["endtime"]               # NOT NULL
            employeeid = request.form["employeeid"]         # FK, NOT NULL
            typename = request.form["typename"]             # FK
            departmentid = request.form["departmentid"]     # FK, NOT NULL

            # Account for null typeName
            if typename is None:
                query = "INSERT INTO Schedules (scheduletype, shift, starttime, endtime, employeeid, departmentid) \
                VALUES( %s, %s, %s, %s, \
                (SELECT employeeid FROM Employees WHERE name=%s),\
                (SELECT departmentid FROM Departments WHERE depname = %s));"
                cur = conn.cursor()
                cur.execute(query, (scheduletype, shift, starttime, endtime, employeeid, departmentid))
                conn.commit()

            # No null inputs
            else:
                query = "INSERT INTO Schedules\
                    (scheduletype, shift, starttime, endtime, employeeid, typename, departmentid)\
                VALUES( %s, %s, %s, %s,\
                (SELECT employeeid FROM Employees WHERE employeeid=%s),\
                (SELECT typename FROM EmploymentTypes WHERE typename = %s),\
                (SELECT departmentid FROM Departments WHERE depname = %s));"
                cur = conn.cursor()
                cur.execute(query, (scheduletype, shift, starttime, endtime, employeeid, typename, departmentid))
                conn.commit()

            # Redirect back to schedules page after executing the add query
            return redirect("/schedules")
    
    if request.method == "GET":
        query = "SELECT * FROM Schedules"
        cur = conn.cursor()
        cur.execute(query)
        schedules_data = cur.fetchall()
        query2 = "SELECT employeeID, name FROM Employees"
        cur = conn.cursor()
        cur.execute(query2)
        employeefk = cur.fetchall()
        query3 = "SELECT departmentID, depName FROM Departments"
        cur = conn.cursor()
        cur.execute(query3)
        departmentfk = cur.fetchall()
        query4 = "SELECT typeName FROM EmploymentTypes"
        cur = conn.cursor()
        cur.execute(query4)
        emptypefk = cur.fetchall() 
        return render_template("add_schedule.j2", schedules_data=schedules_data, 
                               employeefk=employeefk, departmentfk=departmentfk, emptypefk=emptypefk)
