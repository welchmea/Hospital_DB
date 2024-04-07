from flask import Blueprint, render_template, request, redirect
import psycopg2
import os

employType = Blueprint('empTypes', __name__)

# -----------------------------
# - CRUD for Employment Types -
# -----------------------------
DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')


# route for main employmentTypes page
@employType.route("/employmentTypes", methods=["POST", "GET"])
def employmentTypes():

    # Grab employment type data from mySQl and call template to display
    if request.method == "GET":
        # mySQL query to grab all from EmploymentTypes
        query = "SELECT EmploymentTypes.typeName,\
            EmploymentTypes.hoursAllow FROM EmploymentTypes;"
        cur = conn.cursor()
        cur.execute(query)
        employmentTypes_data = cur.fetchall()

        return render_template("employmentTypes.j2", employmentTypes_data=employmentTypes_data)
    
# route for delete functionality, deleting an employment type
@employType.route("/delete_employmentTypes/<string:typeName>")
def delete_employmentTypes(typeName):

    # mySQL query to delete the selection with the passed id
    query = "DELETE FROM EmploymentTypes WHERE typeName = %s;"
    cur = conn.cursor()
    cur.execute(query, (typeName,))
    conn.commit()

    return redirect("/employmentTypes")

# add a new employmentType to the DB
@employType.route("/add_employmentTypes", methods=["POST", "GET"])
def add_employmentTypes():

    if request.method == "GET":
        query = "SELECT * FROM EmploymentTypes"
        cur = conn.cursor()
        cur.execute(query)
        employmentTypes_data = cur.fetchall()
        return render_template('add_employmentTypes.j2', employmentTypes_data=employmentTypes_data)
    
    if request.method == "POST":
        # grab user inputs
        if request.form.get("add_employmentTypes"):
            typeName = request.form["typeName"]
            hoursAllow = request.form["hoursAllow"]

            # no null values 
            query = "INSERT INTO EmploymentTypes (typeName, hoursAllow) VALUES(%s, %s);"
            cur = conn.cursor()
            cur.execute(query, (typeName, hoursAllow))
            conn.commit()

        # redirect back to jobs page after we execute the add query
        return redirect("/employmentTypes")