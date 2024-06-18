from flask import Blueprint, render_template, request, redirect
import psycopg2
import os
# from ...config import load_config

emp_department = Blueprint('department_page', __name__)

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
# config = load_config()
# conn = connect(config)

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')



# route for departments page
@emp_department.route("/departments", methods=["POST", "GET"])
def departments():
    
    departments_data = None
    # Grab department data from mySQl and call template to display
    if request.method == "GET":
        # mySQL query to grab all from Departments
        query = "SELECT Departments.departmentid, Departments.depname,\
            Departments.description FROM Departments;"
        cur = conn.cursor()
        cur.execute(query)
        departments_data = cur.fetchall()

    return render_template("departments.j2", departments_data=departments_data)


# route for delete functionality, deleting a department by id
@emp_department.route("/delete_departments/<int:departmentid>")
def delete_departments(departmentid):

    # mySQL query to delete the department with our passed id
    query = "DELETE FROM Departments WHERE departmentid = %s;"
    cur = conn.cursor()
    cur.execute(query, [departmentid])
    conn.commit()

    # redirect back to department page
    return redirect("/departments")

# route for edit functionality, updating the attributes of a department
# pass the 'id' value of that department on button click (see HTML) via the route
@emp_department.route("/edit_department/<int:departmentid>", methods=["POST", "GET"])
def edit_department(departmentid):
    
    if request.method == "GET":
        # mySQL query to grab the info of the Department with our passed id
        query = "SELECT * FROM Departments WHERE departmentid = %s" % departmentid
        cur = conn.cursor()
        cur.execute(query)
        departments_data = cur.fetchall()
        # render edit template passing our query data
        return render_template("edit_department.j2", departments_data=departments_data)

    # queries to DB using data from edit template
    if request.method == "POST":
        if request.form.get('update_department'):
            # grab user form inputs
            departmentid = departmentid
            depname = request.form["depname"]
            description = request.form["description"]
            # account for null description
            if description == "":
                query = "UPDATE Departments SET depname = %s WHERE Departments.departmentid = %s"
                cur = conn.cursor()
                cur.execute(query, (depname, departmentid))
                conn.commit()

            # no null inputs
            else:
                query = "UPDATE Departments SET depname = %s, description = %s WHERE Departments.departmentid = %s"
                cur = conn.cursor()
                cur.execute(query, [depname, description, departmentid])
                conn.commit()

        # redirect back to main department page
        return redirect("/departments")

# route to add a new department to the DB
@emp_department.route("/add_department", methods=["POST", "GET"])
def add_department():

    depname, description, departments_data = None,None,None
    # button click will render new page 
    if request.method == "GET":
        query = "SELECT * FROM Departments"
        cur = conn.cursor()
        cur.execute(query)
        departments_data = cur.fetchall()
        return render_template('add_department.j2', departments_data=departments_data)
    
    if request.method == "POST":
        if request.form.get("add_department"):
        # grab user form inputs
            depname = request.form["depname"]
            description = request.form["description"]

        # account for null description
        if description == "":
            query = "INSERT INTO Departments (depname) VALUES(%s);"
            cur = conn.cursor()
            cur.execute(query, (depname,))
            conn.commit()

        # no null inputs
        else:
            query = "INSERT INTO Departments (depname, description) VALUES(%s, %s);"
            cur = conn.cursor()
            cur.execute(query, (depname, description))
            conn.commit()

        # redirect back to main page after we execute the add query
        return redirect("/departments")