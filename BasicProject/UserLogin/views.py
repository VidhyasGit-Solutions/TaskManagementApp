from datetime import datetime
from flask import render_template
from UserLogin import runserver

@runserver.route('/')
@runserver.route('/home')
def home():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    return render_template(
        "index.html",
        title = "Welcome to Task Management App",
        message = "Welcome to Task Management App!",
        content = " on " + formatted_now)


@runserver.route('/api/data')
def get_data():
  return runserver.send_static_file('data.json')

@runserver.route('/about')
def about():
    return render_template(
        "about.html",
        title = "About Task Management App",
        content = "About Task Management App.")