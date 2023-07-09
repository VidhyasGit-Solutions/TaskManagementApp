from flask import Flask, render_template, request, redirect, url_for, session
from UserLogin import runserver
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
#import pyodbc
import re
import sqlite3
import os


# MSSQL Database connection details

server = 'localhost\SQLEXPRESS'
database = 'TaskManagementDB'
driver = '{ODBC Driver 17 for SQL Server}'  # Adjust the driver based on your installed version

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

@runserver.route('/')
@runserver.route('/login', methods =['GET', 'POST'])
def login():
    """
    Login Validation and the password is hashed and saved in DB table for security purpose.

    Parameters:
    - NA

    Returns:
    - Renders the next page with message.
    """
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        # Check if input field are provided
        if len(username) == 0:
            print('username does not exist')
            msg = 'Please provide username'
            return render_template('login.html', msg = msg)
        
        if len(password) == 0:
            print('password does not exist')
            msg = 'Please provide password'
            return render_template('login.html', msg = msg)

        # Establish a connection to the SQL Server database
        try:
            print(os.getcwd())
            #Connecting to sqlite
            conn = sqlite3.connect('TaskManagementDB.db')
            cursor = conn.cursor()

            cursor.execute('SELECT Id, username, password FROM useraccounts WHERE username = ?', (username,))
            account = cursor.fetchone()
            print("First DB row:",account)
        except sqlite3.Error as e:
            # Handle the specific SQL exception
            print("An error occurred:", e)
        finally:
            # Close the database connection
            cursor.close
            conn.close
        if account:
            session['loggedin'] = True
            session['id'] = int(account[0])
            session['username'] = account[1]
            hash_password = account[2]
            print("First DB row:",session['username'])
            if check_password_hash(hash_password, password):
                # Passwords match, proceed with authentication
                msg = 'Logged in successfully !'
            else:
                # Passwords do not match
                msg = 'Incorrect password !'

            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username !'
        
    return render_template('login.html', msg = msg)

@runserver.route('/logout')
def logout():
    """
    Logs out the user by clearing all session variables.

    Parameters:
    - NA

    Returns:
    - Renders the Login page.
    """
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# This function just renders the task page
@runserver.route('/tasks')
def tasks():
    print("Getting into Task Screen")
    msg = ''
    return render_template('tasks.html')

@runserver.route('/addtask', methods =['GET', 'POST'])
def addtask():
    """
    Add Task and Saves into taskdetails DB table.

    Parameters:
    - NA

    Returns:
    - Renders the taskList page.
    """
    print("Getting into AddTask function")
    msg = ''
    if request.method == 'POST' and 'tasktitle' in request.form and 'taskstatus' in request.form :
        print("Getting into If block of AddTask function")
        tasktitle = request.form['tasktitle']
        taskdescription = request.form['taskdescription']
        taskcategory = request.form['taskcategory']
        taskpriority = request.form['taskpriority']
        taskstatus = request.form['taskstatus']
        taskduedate = request.form['taskduedate']
        user_id = session.get('id')
        
        
        # Establish a connection to the SQL Server database
        try:
            #Connecting to sqlite
            conn = sqlite3.connect('TaskManagementDB.db')
            cursor = conn.cursor()

            # Example insert statement with datetime field
            insert_query = "INSERT INTO taskdetails (UserId,name,description,priority,category,status,duedate) VALUES (?, ?, ?, ?, ?, ?, ?)"
            values = (user_id, tasktitle, taskdescription, taskpriority, taskcategory, taskstatus, taskduedate)

            # Execute the insert statement
            cursor.execute(insert_query, values)

            conn.commit()
            print("Successfully Inserted the task row")
        except sqlite3.Error as e:
            # Handle the specific SQL exception
            print("An error occurred:", e)
        finally:
            cursor.close
            conn.close
    return redirect(url_for('tasklist'))

@runserver.route('/updatetask/<taskId>', methods =['GET', 'POST'])
def updatetask(taskId):
    """
    Update Task and updates into taskdetails DB table.

    Parameters:
    - taskId - Passed from the taskList table

    Returns:
    - Renders the taskList page.
    """
    if request.method == 'POST' and 'tasktitle' in request.form and 'taskstatus' in request.form :
        tasktitle = request.form['tasktitle']
        taskdescription = request.form['taskdescription']
        taskcategory = request.form['taskcategory']
        taskpriority = request.form['taskpriority']
        taskstatus = request.form['taskstatus']
        taskduedate = request.form['taskduedate']

        # Establish a connection to the SQL Server database
        try:
            #Connecting to sqlite
            conn = sqlite3.connect('TaskManagementDB.db')
            cursor = conn.cursor()
               
            cursor.execute('UPDATE taskdetails SET name = ?, description = ?, priority = ?, category = ?, status = ?, duedate = ? WHERE taskId = ?', (tasktitle, taskdescription, taskpriority, taskcategory, taskstatus, taskduedate, taskId))
            conn.commit()
        except sqlite3.Error as e:
            # Handle the specific SQL exception
            print("An error occurred:", e)
        finally:
            cursor.close
            conn.close
    return redirect(url_for('tasklist'))

@runserver.route('/tasklist', methods =['GET', 'POST'])
def tasklist():
    """
    Fetch List of tasks from taskdetails DB table based on the userId.

    Parameters:
    - UserId is fetched from session variable

    Returns:
    - Renders the taskList page.
    """
    msg = 'You have successfully created the task !'

    user_id = session.get('id')
    print("Inside the taskList function, check the user_id",user_id)
    # Establish a connection to the SQL Server database
    try:
        #Connecting to sqlite
        conn = sqlite3.connect('TaskManagementDB.db')
        cursor = conn.cursor()

        cursor.execute('SELECT taskId,name,category,priority,status FROM taskdetails WHERE UserId = ?', (user_id,))
        taskLists = cursor.fetchall()
        print("TaskList :",taskLists)
    except sqlite3.Error as e:
        # Handle the specific SQL exception
        print("An error occurred:", e)
    finally:
        cursor.close
        conn.close
    return render_template('taskList.html', taskLists = taskLists)

@runserver.route('/delete/<taskId>', methods =['GET', 'POST'])
def delete(taskId):
    """
    Delete Task and updates into taskdetails DB table.

    Parameters:
    - taskId - Passed from the taskList table

    Returns:
    - Renders the taskList page.
    """

    # Establish a connection to the SQL Server database
    try:
        #Connecting to sqlite
        conn = sqlite3.connect('TaskManagementDB.db')
        cursor = conn.cursor()
        print("Inside of Delete function - taskId - ",taskId)
        cursor.execute('DELETE FROM taskdetails WHERE taskId = ?', (taskId,))
        print("Inside of Delete function - taskId - ",taskId)
        conn.commit()
        print("Inside of Delete function - taskId - ",taskId)
        
        user_id = session.get('id')
        print("Inside of Delete function - user_id - ",user_id)
        cursor.execute('SELECT taskId,name,category,priority,status FROM taskdetails WHERE UserId = ?', (user_id,))
        taskLists = cursor.fetchall()
    except sqlite3.Error as e:
        # Handle the specific SQL exception
        print("An error occurred:", e)
    finally:
        cursor.close
        conn.close
    return render_template('taskList.html', taskLists=taskLists)

@runserver.route('/display/<taskId>', methods =['GET', 'POST'])
def display(taskId):
    """
    Fetch the corresponding task to display from taskdetails DB table.

    Parameters:
    - taskId - Passed from the taskList table

    Returns:
    - Renders the taskDisplay page.
    """
    # Establish a connection to the SQL Server database
    try:
        #Connecting to sqlite
        conn = sqlite3.connect('TaskManagementDB.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT taskId, UserId, name, description, category, priority, status, duedate FROM taskdetails WHERE taskId = ?', (taskId,))
        taskdisplay = cursor.fetchone()
        print("Fetched Task Detail Row :",taskdisplay)
    except sqlite3.Error as e:
        # Handle the specific SQL exception
        print("An error occurred:", e)
    finally:
        cursor.close
        conn.close
    return render_template('taskdisplay.html', taskdisplay = taskdisplay)

@runserver.route('/register', methods =['GET', 'POST'])
def register():
    """
    Register User first time and save the details to useraccounts DB table.

    Parameters:
    - NA

    Returns:
    - Renders the register page with msg.
    """
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if input values are provided
        if len(username) == 0:
            print('username does not exist')
            msg = 'Please provide username'
            return render_template('register.html', msg = msg)
        
        if len(password) == 0:
            print('password does not exist')
            msg = 'Please provide password'
            return render_template('register.html', msg = msg)

        if len(email) == 0:
            print('email does not exist')
            msg = 'Please provide email'
            return render_template('register.html', msg = msg)
        
        password_hash = generate_password_hash(password)
        # Establish a connection to the SQL Server database
        try:
            #Connecting to sqlite
            conn = sqlite3.connect('TaskManagementDB.db')
            cursor = conn.cursor()

            cursor.execute('SELECT Id FROM useraccounts WHERE username = ?', (username,))
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
                cursor.execute('INSERT INTO useraccounts (username,password,email) VALUES (?, ?, ?)', (username, password_hash, email))
                conn.commit()
                msg = 'You have successfully registered !'
        except sqlite3.Error as e:
            # Handle the specific SQL exception
            print("An error occurred:", e)
        finally:
            cursor.close
            conn.close
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)