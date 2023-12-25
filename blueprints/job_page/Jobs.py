from flask import Blueprint, render_template, request, redirect
import psycopg2

emp_job = Blueprint('job_page', __name__)


def get_connection():
    conn = psycopg2.connect(host='ec2-3-232-218-211.compute-1.amazonaws.com', database='d6af5e5pibqrf1', user='xbeltbfqliosyk', password='294e9b67571b4e7e9ed12a10d8f0a5591750f681382b0a8193eeece39e5fde68')
    return conn


conn = get_connection()

# -----------------------------
# --- CRUD for Jobs ----
# -----------------------------

# route for jobs page
@emp_job .route("/jobs", methods=["POST", "GET"])
def jobs():
    # Grab jobs data from mySQl and call template to display
    if request.method == "GET":

        # mySQL query to grab all from Jobs
        query = "SELECT Jobs.jobID, Jobs.jobName, Jobs.description FROM Jobs;"
        cur = conn.cursor()
        cur.execute(query)
        jobs_data = cur.fetchall()
        return render_template("jobs.j2", jobs_data=jobs_data)
    
# route for delete functionality, deleting a job by id
@emp_job .route("/delete_jobs/<int:jobID>")
def delete_jobs(jobID):

    # mySQL query to delete the job with our passed id
    query = "DELETE FROM Jobs WHERE jobID = '%s';"
    cur = conn.cursor()
    cur.execute(query, (jobID,))
    conn.commit()

    # redirect back to job page
    return redirect("/jobs")

# the pass the 'id' value of the job on button click (see HTML) via the route
@emp_job .route("/edit_job/<int:jobID>", methods=["POST", "GET"])
def edit_job(jobID):
    if request.method == "GET":
        # mySQL query to grab the info of the Job with our passed id
        query = "SELECT * FROM Jobs WHERE jobID = %s" % (jobID)
        cur = conn.cursor()
        cur.execute(query)
        jobs_data = cur.fetchall()

        return render_template("edit_job.j2", jobs_data=jobs_data)

    # post changed data to the DB
    if request.method == "POST":

        # grab user form inputs
        if request.form.get('Update_Job'):
            jobID = request.form["jobID"]
            jobName = request.form["jobName"]
            description = request.form["description"]

        # account for null description
        if description == "":
            query = "UPDATE Jobs SET jobName = %s WHERE Jobs.jobID = %s"
            cur = conn.cursor()
            cur.execute(query, (jobName, jobID))
            conn.commit()

        # no null inputs
        else:
            query = "UPDATE Jobs SET jobName = %s, description = %s WHERE Jobs.jobID = %s"
            cur = conn.cursor()
            cur.execute(query, (jobName, description, jobID))
            conn.commit()

        # redirect back to jobs page after we execute the update query
        return redirect("/jobs")

# route to add a new job to the DB
@emp_job .route("/add_job", methods=["POST", "GET"])
def add_job():

    # button click will render a new template/page
    if request.method == "GET":
        query = "SELECT * FROM Jobs"
        cur = conn.cursor()
        cur.execute(query)
        jobs_data = cur.fetchall()
        return render_template('add_job.j2', jobs_data=jobs_data)
    
    # reroute back with form data
    if request.method == "POST":

        if request.form.get("add_job"):
            jobName = request.form["jobName"]
            description = request.form["description"]

        # account for null description
        if description == "":
            query = "INSERT INTO Jobs (jobName) VALUES( %s);"
            cur = conn.cursor()
            cur.execute(query, (jobName))
            conn.commit()

        # no null inputs
        else:
            query = "INSERT INTO Jobs (jobName, description) VALUES(%s, %s);"
            cur = conn.cursor()
            cur.execute(query, (jobName, description))
            conn.commit()

        # redirect back to jobs page after we execute the add query
        return redirect("/jobs")