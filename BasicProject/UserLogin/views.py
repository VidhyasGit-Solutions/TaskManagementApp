from flask import Flask
from UserLogin import app

@app.route('/')
@app.route('/home')
def home():
    return "Welcome to Task Management App!"