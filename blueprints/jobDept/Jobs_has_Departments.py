from flask import Blueprint, render_template, request, redirect
import os
import psycopg2
from config import load_config


jobdepartment = Blueprint('jobDept', __name__,)

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
# ----------------------------------------
# - CRUD for Jobs has Departments------- -
# ----------------------------------------

# Route for Job Departments page
@jobdepartment.route("/jobdept", methods=["GET"])
def jobdept():
    # Grabs Job Departments data from mySQl and call template to display
    if request.method == "GET":
        # mySQL query to grab all from Job Departments
        query = "SELECT Jobs_has_Departments.jobDeptID, \
            Jobs.jobName, Departments.depName \
            FROM Jobs_has_Departments \
            LEFT JOIN Jobs ON Jobs.jobID = Jobs_has_Departments.jobID \
            LEFT JOIN Departments ON Departments.departmentID = Jobs_has_Departments.departmentID;"
        cur = conn.cursor()
        cur.execute(query)
        jobdept_data = cur.fetchall()

    return render_template("jobdept.j2", jobdept_data=jobdept_data)

# Route for delete functionality, deleting selected Job Departments by jobDeptID
@jobdepartment.route("/delete_job_dept/<int:jobDeptID>")
def delete_job_dept(jobDeptID):
    # mySQL query to delete the Job Department with passed id
    query = "DELETE FROM Jobs_has_Departments WHERE jobDeptID = '%s';"
    cur = conn.cursor()
    cur.execute(query, (jobDeptID,))
    conn.commit()

    # Redirect back to Job Departments page
    return redirect("/jobdept")

@jobdepartment.route("/add_job_dept", methods=["POST", "GET"])
def add_job_dept():
    # Inserts data about a new job department into the job departments entity
    if request.method == "POST":
        if request.form.get("add_job_dept"):
        # Grab user form inputs
            jobID = request.form["jobID"]
            departmentID = request.form["departmentID"] 

        # Account for null jobID
        if jobID == None:
            query = " INSERT INTO Jobs_has_Departments(departmentID)\
                VALUES(( SELECT departmentID FROM Departments WHERE depName = %s));"
            cur = conn.cursor()
            cur.execute(query, (departmentID))
            conn.commit()

        # Account for null departmentID
        if departmentID == None:
            query = "INSERT INTO Employees (jobID) \
            VALUES ((SELECT jobID FROM Jobs WHERE jobName = %s));"
            cur = conn.cursor()
            cur.execute(query, (jobID))
            conn.commit()

        # No null inputs
        else:
            query = "INSERT INTO Jobs_has_Departments(jobID, departmentID)\
                VALUES((SELECT jobID FROM Jobs WHERE jobName = %s),\
                (SELECT departmentID FROM Departments WHERE depName = %s));"
            cur = conn.cursor()
            cur.execute(query, (jobID, departmentID))
            conn.commit()

        # Redirect back to departments page after executing the add query
        return redirect("/jobdept")

    if request.method == "GET":
        query = "SELECT * FROM Jobs_has_Departments"
        cur = conn.cursor()
        cur.execute(query)
        jobdept_data = cur.fetchall()
        query3 = "SELECT jobID, jobName FROM Jobs;"
        cur = conn.cursor()
        cur.execute(query3)
        jobIDFK = cur.fetchall()
        query4 = "SELECT departmentID, depName FROM Departments"
        cur = conn.cursor()
        cur.execute(query4)
        departmentFK = cur.fetchall() 
        return render_template("add_job_dept.j2", jobdep_data=jobdept_data, jobIDFK=jobIDFK, departmentFK=departmentFK)
    
@jobdepartment.route("/edit_jobdept/<int:jobDeptID>", methods=["POST", "GET"])
def edit_jobdept(jobDeptID):
    if request.method == "GET":
        # mySQL query to grab the info of the Employee with passed id
        query = "SELECT * FROM Jobs_has_Departments WHERE jobDeptID = %s" % (jobDeptID)
        cur = conn.cursor()
        cur.execute(query)
        jobdept_data = cur.fetchall()
        query3 = "SELECT jobID, jobName FROM Jobs;"
        cur = conn.cursor()
        cur.execute(query3)
        jobIDFK = cur.fetchall()
        query4 = "SELECT departmentID, depName FROM Departments"
        cur = conn.cursor()
        cur.execute(query4)
        departmentFK = cur.fetchall() 

        # Render edit_department page passing query data to the edit_department template
        return render_template("edit_jobdept.j2", jobdept_data=jobdept_data, jobIDFK=jobIDFK, departmentFK=departmentFK )

    # Conditional to alter table contents in database
    if request.method == "POST":
        # grab user form inputs
        if request.form.get('edit_jobdept'):
            jobDeptID = request.form['jobDeptID']
            jobID = request.form["jobID"]
            departmentID = request.form["departmentID"] 

            # No null inputs
            query = "UPDATE Jobs_has_Departments SET jobID = %s, departmentID = %s WHERE jobDeptID = %s"
            cur = conn.cursor()
            cur.execute(query, (jobID, departmentID, jobDeptID))
            conn.commit()

        # Redirect back to departments page after executing the update query
        return redirect("/jobdept")