from fileinput import filename
import os
from turtle import title
from webappfiles import dbconnect

import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, request, flash,  redirect, session, url_for
from . import mail

from flask_mail import Mail, Message
mail = Mail()


auth = Blueprint('auth', __name__)


# Sign-up Houseowner

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['txtfn']
        last_name = request.form['txtln']
        email = request.form['txtmail']
        password1 = request.form['txtpassword']
        password2 = request.form['txtpass2']
        Postal_Address = request.form['txtaddress']
        district = request.form['txtdistrict']

        cur, con = dbconnect.get_connection()
        sql = "select Email_Address from tblhouseowner where Email_Address= %s"
        val = (email,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        count = cur.rowcount

        if (count > 0):
            flash('User already exists.', category='error')
        elif (len(email) < 5):
            flash('Email must be greater than 4 characters.', category='error')
        elif (len(first_name) < 3):
            flash('First name must be greater than 2 characters.', category='error')
        elif (password1 != password2):
            flash('Passwords don\'t match.', category='error')
        elif (len(password1) < 3):
            flash('Password must be at least 3 characters.', category='error')
        else:
            password1 = generate_password_hash(password1, method='sha256')
            sql2 = "INSERT into tblhouseowner (Fname, Lname, Email_Address, password, Postal_Address, District) values (%s,%s,%s,%s,%s,%s)"
            val2 = (first_name, last_name, email,
                    password1, Postal_Address, district)
            cur.execute(sql2, val2)
            con.commit()
            msg = str(cur.rowcount) + " record added, "
            msg1 = Message('Job Portal',
                           sender='zainabbaichoo01@gmail.com', recipients=[email])
            msg1.body = "Welcome to Job Portal " + first_name + "\r\n"
            msg1.body += "You are now a member and may access the website \r\n "
            msg1.body += "@ http://localhost:5000/"
            mail.send(msg1)
            flash(msg + ' account created!', category='success')
        return redirect(url_for('views.profileho'))
    return render_template("signup.html")


# Login housekeeper

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['txtemail']
        pwd = request.form['txtpwd']
        cur, con = dbconnect.get_connection()
        sql = "select Password, Email_Address, keeper_id, Fname from tblhousekeeper where Email_Address= %s"
        val = (email,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        count = cur.rowcount

        for row in rows:
            passw = row[0]

            if (count > 0):
                if check_password_hash(passw, pwd):
                    session['hkid'] = rows[0][2]
                    session['fname'] = rows[0][3]
                    flash('Logged in successfully!', category='success')
                    return redirect(url_for('views.profilehk'))
                else:
                    flash('Incorrect password, pls try again.', category='error')
            else:
                flash('Email does not exist.', category='error')
    return render_template("login.html")

# Logout housekeeper


@auth.route('/logout/')
def logout():
    session.pop('hkid')
    return redirect('/index')


# Login houseowner

@auth.route('/login2', methods=['GET', 'POST'])
def login2():
    if request.method == 'POST':
        email = request.form['txtemail']
        pwd = request.form['txtpwd']
        cur, con = dbconnect.get_connection()
        sql = "select password, Email_Address, Owner_id, Fname from tblhouseowner where Email_Address= %s"
        val = (email,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        count = cur.rowcount

        for row in rows:
            passw = row[0]

        if (count > 0):
            if check_password_hash(passw, pwd):
                session['hoid'] = rows[0][2]
                session['fname'] = rows[0][3]
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.profileho'))
            else:
                flash('Incorrect password, pls try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login2.html")

# Logout houseowner


@auth.route('/logout2/')
def logout2():
    session.pop('hoid')
    return redirect('/index')


# Register Housekeeper

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        title = request.form['txttitle']
        first_name = request.form['txtfn']
        last_name = request.form['txtln']
        email = request.form['txtmail']
        password1 = request.form['txtpassword']
        password2 = request.form['txtpass2']
        Postal_Address = request.form['txtpostal']
        contact = request.form['txtcontact']
        Date_of_birth = request.form['txtdob']
        H_Qualification = request.form['txtqualification']
        f = request.form['txtfilecv']
        skill = request.form['txtskill']

        cur, con = dbconnect.get_connection()
        sql = "select Email_Address from tblhousekeeper where Email_Address= %s"
        val = (email,)
        cur.execute(sql, val)
        rows = cur.fetchall()
        count = cur.rowcount

        if (count > 0):
            flash('User already exists.', category='error')
        elif (len(email) < 5):
            flash('Email must be greater than 4 characters.', category='error')
        elif (len(first_name) < 3):
            flash('First name must be greater than 2 characters.', category='error')
        elif (password1 != password2):
            flash('Passwords don\'t match.', category='error')
        elif (len(password1) < 3):
            flash('Password must be at least 3 characters.', category='error')
        else:
            password1 = generate_password_hash(password1, method='sha256')
            sql2 = "INSERT into tblhousekeeper (Title, Fname, Lname, Email_Address, Password, Postal_Address, Contact_number, Date_of_birth, H_Qualification, Curriculumn_Vitae, Skills_id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val2 = (title, first_name, last_name, email,
                    password1, Postal_Address, contact, Date_of_birth, H_Qualification, f, skill)
            cur.execute(sql2, val2)
            con.commit()
            msg = str(cur.rowcount) + " record added, "
            msg1 = Message('Job Portal',
                           sender='zainabbaichoo01@gmail.com', recipients=[email])
            msg1.body = "Welcome to Job Portal " + first_name + "\r\n"
            msg1.body += "You are now a member and may access the website \r\n "
            msg1.body += "@ http://localhost:5000/"
            mail.send(msg1)
            flash(msg + ' account created!', category='success')
        return redirect(url_for('views.profilehk'))
    return render_template("register.html", msg=msg, title=title)
