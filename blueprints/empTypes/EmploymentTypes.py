from flask import Blueprint, render_template, request, redirect
import psycopg2
import os
from ...config import load_config 

employType = Blueprint('empTypes', __name__)

# -----------------------------
# - CRUD for Employment Types -
# -----------------------------
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


# route for main employmentTypes page
@employType.route("/employment_types", methods=["POST", "GET"])
def employment_types():

    # Grab employment type data from mySQl and call template to display
    if request.method == "GET":
        # mySQL query to grab all from EmploymentTypes
        query = "SELECT EmploymentTypes.typeName,\
            EmploymentTypes.hoursAllow FROM EmploymentTypes;"
        cur = conn.cursor()
        cur.execute(query)
        employmenttypes_data = cur.fetchall()

        return render_template("employmentTypes.j2", employmenttypes_data=employmenttypes_data)
    
# route for delete functionality, deleting an employment type
@employType.route("/delete_employmenttypes/<string:typename>")
def delete_employmenttypes(typename):

    # mySQL query to delete the selection with the passed id
    query = "DELETE FROM EmploymentTypes WHERE typename = %s;"
    cur = conn.cursor()
    cur.execute(query, (typename,))
    conn.commit()

    return redirect("/employment_types")

# add a new employmentType to the DB
@employType.route("/add_employmenttypes", methods=["POST", "GET"])
def add_employmenttypes():

    if request.method == "GET": 
        query = "SELECT * FROM EmploymentTypes"
        cur = conn.cursor()
        cur.execute(query)
        employment_types_data = cur.fetchall()
        return render_template('add_employmentTypes.j2', employment_types_data=employment_types_data)
    
    if request.method == "POST":
        # grab user inputs
        if request.form.get("add_employmenttypes"):
            typename = request.form["typename"]
            hoursallow = request.form["hoursallow"]

            # no null values 
            query = "INSERT INTO EmploymentTypes (typename, hoursallow) VALUES(%s, %s);"
            cur = conn.cursor()
            cur.execute(query, (typename, hoursallow))
            conn.commit()

        # redirect back to jobs page after we execute the add query
        return redirect("/employment_types")