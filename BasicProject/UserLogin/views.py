from flask import Flask, render_template, request, redirect, url_for, session
from UserLogin import runserver
import pyodbc
import re

# Database connection details

server = 'localhost\SQLEXPRESS'
database = 'TaskManagementDB'
driver = '{ODBC Driver 17 for SQL Server}'  # Adjust the driver based on your installed version

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

def create_db_connection():
    return pyodbc.connect(conn_str)

@runserver.route('/')
@runserver.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        # Establish a connection to the SQL Server database
        conn = create_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM dbo.useraccounts WHERE username = ? AND password = ?', (username, password))
        account = cursor.fetchone()
        print("First DB row:",account)
        if account:
            session['loggedin'] = True
            session['id'] = int(account[0])
            session['username'] = account[1]
            print("First DB row:",session['username'])
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@runserver.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@runserver.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Establish a connection to the SQL Server database
        conn = create_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM dbo.useraccounts WHERE username = ?', (username))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO dbo.useraccounts (username,password,email) VALUES (?, ?, ?)', (username, password, email))
            conn.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)