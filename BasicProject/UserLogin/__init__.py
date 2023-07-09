from flask import Flask
import secrets
import sqlite3

runserver = Flask(__name__, static_folder='static')
# Generate a secure secret key
secret_key = secrets.token_hex(16)
runserver.secret_key = secret_key

import UserLogin.views

#Connecting to sqlite
conn = sqlite3.connect('TaskManagementDB.db')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Creating table as per requirement
sql ='''CREATE TABLE  IF NOT EXISTS useraccounts (
Id     INTEGER PRIMARY KEY AUTOINCREMENT,
username   TEXT  NOT NULL,
password   TEXT  NOT NULL,
email      TEXT  NOT NULL,
created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)'''

cursor.execute(sql)
print("useraccounts Table created successfully........")

#Creating table as per requirement
sql ='''CREATE TABLE  IF NOT EXISTS taskdetails (
taskId	INTEGER  PRIMARY KEY  AUTOINCREMENT,
UserId  INTEGER	 NOT NULL,
name   	TEXT     NOT NULL,
description   TEXT   NULL,
priority   	TEXT     NULL,
category   	TEXT     NULL,
status      TEXT     NOT NULL,
duedate 	DATETIME   NOT NULL,
FOREIGN KEY (UserId) REFERENCES useraccounts(Id)
)'''

cursor.execute(sql)
print("taskdetails Table created successfully........")

# Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()