from flask import Blueprint, render_template, request, session, redirect, flash

import mysql.connector
from webappfiles import dbconnect

from datetime import datetime
import os
cur, con = dbconnect.get_connection()

views = Blueprint('views', __name__)
# referring to the default page via the “/” route


@views.route("/index/")
def index():
    return render_template("index.html")


@views.route("/housekeeper/")
def house_keeper():
    return render_template("housekeeper.html")


@views.route("/houseowner/")
def house_owner():
    return render_template("houseowner.html")


@views.route("/login/")
def log_in():
    return render_template("login.html")


@views.route("/signup/")
def sign_up():
    return render_template("signup.html")


# populate skills
@views.route("/registration/")
def registration():
    cur.execute("SELECT * FROM tblskills")
    rows = cur.fetchall()
    return render_template('register.html', rows=rows)

# view job


@views.route("/viewjob/")
def view_job():
    cur.execute("SELECT * FROM tbljobs")

    rows = cur.fetchall()
    return render_template("viewjobs.html", rows=rows)

# add job


@views.route("/addjob/")
def addjob():
    if 'Owner_id' in session:
        cur, con = dbconnect.get_connection()
        sql = "SELECT Owner_id FROM tblhouseowner where Owner_id = %s"
        val = (session.get('Owner_id'),)
        cur.execute(sql, val)
        rows1 = cur.fetchall()
    return render_template("job.html")


@views.route("/savedetails", methods=["POST"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            jobdesc = request.form["txtdes"]
            jobreference = request.form["txtref"]
            title = request.form["txttitle"]
            salary = request.form["txtprice"]
            dt = request.form["txtdate"]

            sql = "INSERT into tbljobs(Job_Desc,Job_Ref,Job_Title,Salary,Closing_date,Owner_id) values (%s,%s,%s,%s,%s,%s)"
            # add the form variables for each column
            val = (jobdesc, jobreference, title,
                   salary, dt, session.get('Owner_id'))
            cur.execute(sql, val)
            con.commit()
            msg = str(cur.rowcount) + " Job added"
        except Exception as e:
            con.rollback()
            msg = "Job cannot be added " + str(e)
        finally:
            # pass the msg variable to the return statement
            return render_template("job.html", msg=msg, title=title)
            con.close()


# profile hk

@views.route("/profilehk/")
def profilehk():
    if 'hkid' in session:
        cur, con = dbconnect.get_connection()
        sql = "SELECT * FROM tblhousekeeper where keeper_id = %s"
        val = (session.get('hkid'),)
        cur.execute(sql, val)
        rows = cur.fetchall()
        return render_template('profile_hk.html', rows=rows)
    else:
        return redirect('/index')


# update hk

@views.route("/updateprofilehk/", methods=["POST"])
def updateprofilehk():
    if request.method == "POST":
        email = request.form['txtemail']
        first_name = request.form['txtfn']
        last_name = request.form['txtln']
        try:
            cur, con = dbconnect.get_connection()
            sql = "UPDATE tblhousekeeper SET Email_Address = %s, Fname = %s, Lname = %s where keeper_id = %s"
            val = (email, first_name, last_name, session.get('hkid'))
            cur.execute(sql, val)
            con.commit()
            msg = str(cur.rowcount) + " record successfully updated"
            flash(msg, category='success')
        except:
            msg = "Cannot be updated"
            flash(msg, category='error')
        finally:
            return render_template("index.html", msg=msg)


# profile housekeeper

@views.route("/profileho/")
def profileho():
    if 'hoid' in session:
        cur, con = dbconnect.get_connection()
        sql = "SELECT * FROM tblhouseowner where Owner_id = %s"
        val = (session.get('hoid'),)
        cur.execute(sql, val)
        rows = cur.fetchall()
        return render_template('profile_ho.html', rows=rows)
    else:
        return redirect('/index')


# update houseowner

@views.route("/updateprofileho/", methods=["GET", "POST"])
def updateprofileho():
    if request.method == "POST":
        email = request.form['txtemail']
        first_name = request.form['txtfn']
        last_name = request.form['txtln']
        try:
            cur, con = dbconnect.get_connection()
            sql = "UPDATE tblhouseowner SET Email_Address = %s, Fname = %s, Lname = %s where Owner_id = %s"
            val = (email, first_name, last_name, session.get('hoid'))
            cur.execute(sql, val)
            con.commit()
            msg = str(cur.rowcount) + " record successfully updated"
            flash(msg, category='success')
        except:
            msg = "Cannot be updated"
            flash(msg, category='error')
        finally:
            return render_template("index.html", msg=msg)


# Search Jobs
@views.route("/searchjb/", methods=["GET"])
def searchjob():
    # retrieve the querystring txtlang from the URL
    title = request.args.get("txttitle")
    try:
        sql = "select * from tbljobs WHERE Job_Title= %s"
        val = (title,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        msg = str(cur.rowcount) + " record found!"
    except:
        msg = "There was an issue while searching!"
    finally:
        return render_template("search.html", msg=msg, rows=rows, title=title)


# Search Skills

@views.route("/searchskills/", methods=["GET"])
def searchskills():
    # retrieve the querystring txtlang from the URL
    title = request.args.get("txtsk")
    try:
        sql = "select * from tblhousekeeper hk INNER JOIN tblskills sk ON (hk.Skills_id=sk.Skills_id) where Skills_name = %s"
        val = (title,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        msg = str(cur.rowcount) + " record found!"
    except:
        msg = "There was an issue while searching!"
    finally:
        return render_template("searchskills.html", msg=msg, rows=rows, title=title)


# Joblisting

@views.route("/joblisting/")
def job_listing():
    cur, con = dbconnect.get_connection()
    cur.execute("SELECT * FROM tbljobs")
    rows = cur.fetchall()
    return render_template('Job_listing.html', rows=rows)


# Job updating

@views.route("/updatejob/")
def update_job():
    return render_template("updatejob.html")


@views.route("/updatejob/", methods=["POST"])
def updatejob():
    # retrieve the form values

    salary = request.form["txtprice"]
    ref = request.form["txtref"]

    try:
        sql = "UPDATE tbljobs SET Salary = %s where Job_Ref = %s"
        val = (salary, ref)
        cur.execute(sql, val)
        con.commit()
        msg = str(cur.rowcount) + " record successfully updated"
    except:
        msg = "Cannot be updated"
    finally:
        return render_template("updatejob.html", msg=msg)


# Apply for a job
@views.route("/application/")
def application():
    cur.execute(
        "SELECT * FROM tbljobs jb INNER JOIN tblhouseowner ho on (jb.Job_id=ho.Owner_id)")
    job = cur.fetchall()
    return render_template("apply.html", job=job)


@views.route("/submit_application/", methods=['GET', 'POST'])
def submit_app():
    try:
        if request.method == 'POST':
            title = request.form['txttitle']
            date = request.form['txtdate']
            sql = "INSERT into tblapplicationform (Interview_date, keeper_id) values (%s, %s)"
            val = (title, date, session.get('keeper_id'))
            cur.execute(sql, val)
            con.commit()
            msg = str(cur.rowcount) + " Apply successfully!"
    except:
        msg = "Cannot apply"
    finally:
        return render_template("apply.html", msg=msg)
