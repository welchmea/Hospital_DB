from flask import Blueprint, render_template, request, redirect
import os
import psycopg2
# from ...config import load_config


jobdepartment = Blueprint('jobDept', __name__,)

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


# ----------------------------------------
# - CRUD for Jobs has Departments------- -
# ----------------------------------------


# Route for Job Departments page
@jobdepartment.route("/jobdept", methods=["GET"])
def jobdept():
    
    jobdept_data = None
    # Grabs Job Departments data from mySQl and call template to display
    if request.method == "GET":
        # mySQL query to grab all from Job Departments
        query = "SELECT Jobs_has_Departments.jobdeptid, \
            Jobs.jobname, Departments.depname \
            FROM Jobs_has_Departments \
            LEFT JOIN Jobs ON Jobs.jobid = Jobs_has_Departments.jobid \
            LEFT JOIN Departments ON Departments.departmentid = Jobs_has_Departments.departmentid;"
        cur = conn.cursor()
        cur.execute(query)
        jobdept_data = cur.fetchall()

    return render_template("jobdept.j2", jobdept_data=jobdept_data)


# Route for delete functionality, deleting selected Job Departments by jobdeptid
@jobdepartment.route("/delete_job_dept/<int:jobdeptid>")
def delete_job_dept(jobdeptid):
    # mySQL query to delete the Job Department with passed id
    query = "DELETE FROM Jobs_has_Departments WHERE jobdeptid = '%s';"
    cur = conn.cursor()
    cur.execute(query, (jobdeptid,))
    conn.commit()

    # Redirect back to Job Departments page
    return redirect("/jobdept")


@jobdepartment.route("/add_job_dept", methods=["POST", "GET"])
def add_job_dept():
    
    # Inserts data about a new job department into the job departments entity
    if request.method == "POST":
        if request.form.get("add_job_dept"):
            # Grab user form inputs
            jobid = request.form["jobid"]
            departmentid = request.form["departmentid"] 

            # Account for null jobid
            if jobid is None:
                query = " INSERT INTO Jobs_has_Departments(departmentid)\
                    VALUES(( SELECT departmentid FROM Departments WHERE depname = %s));"
                cur = conn.cursor()
                cur.execute(query, departmentid)
                conn.commit()

            # Account for null departmentid
            if departmentid is None:
                query = "INSERT INTO Employees (jobid) \
                VALUES ((SELECT jobid FROM Jobs WHERE jobname = %s));"
                cur = conn.cursor()
                cur.execute(query, jobid)
                conn.commit()

            # No null inputs
            else:
                query = "INSERT INTO Jobs_has_Departments(jobid, departmentid)\
                    VALUES((SELECT jobid FROM Jobs WHERE jobname = %s),\
                    (SELECT departmentid FROM Departments WHERE depname = %s));"
                cur = conn.cursor()
                cur.execute(query, (jobid, departmentid))
                conn.commit()

            # Redirect back to departments page after executing the add query
            return redirect("/jobdept")

    if request.method == "GET":
        query = "SELECT * FROM Jobs_has_Departments"
        cur = conn.cursor()
        cur.execute(query)
        jobdept_data = cur.fetchall()
        query3 = "SELECT jobid, jobname FROM Jobs;"
        cur = conn.cursor()
        cur.execute(query3)
        jobidfk = cur.fetchall()
        query4 = "SELECT departmentid, depname FROM Departments"
        cur = conn.cursor()
        cur.execute(query4)
        departmentfk = cur.fetchall() 
        return render_template("add_job_dept.j2", jobdep_data=jobdept_data, jobidfk=jobidfk, departmentfk=departmentfk)


@jobdepartment.route("/edit_jobdept/<int:jobdeptid>", methods=["POST", "GET"])
def edit_jobdept(jobdeptid):
    if request.method == "GET":
        # mySQL query to grab the info of the Employee with passed id
        query = "SELECT * FROM Jobs_has_Departments WHERE jobdeptid = %s" % jobdeptid
        cur = conn.cursor()
        cur.execute(query)
        jobdept_data = cur.fetchall()
        query3 = "SELECT jobid, jobname FROM Jobs;"
        cur = conn.cursor()
        cur.execute(query3)
        jobidfk = cur.fetchall()
        query4 = "SELECT departmentid, depname FROM Departments"
        cur = conn.cursor()
        cur.execute(query4)
        departmentfk = cur.fetchall() 

        # Render edit_department page passing query data to the edit_department template
        return render_template("edit_jobdept.j2", jobdept_data=jobdept_data, jobidfk=jobidfk,
                               departmentfk=departmentfk)

    # Conditional to alter table contents in database
    if request.method == "POST":
        # grab user form inputs
        if request.form.get('edit_jobdept'):
            jobdeptid = request.form['jobdeptid']
            jobid = request.form["jobid"]
            departmentid = request.form["departmentid"] 

            # No null inputs
            query = "UPDATE Jobs_has_Departments SET jobid = %s, departmentid = %s WHERE jobdeptid = %s"
            cur = conn.cursor()
            cur.execute(query, (jobid, departmentid, jobdeptid))
            conn.commit()

        # Redirect back to departments page after executing the update query
        return redirect("/jobdept")
