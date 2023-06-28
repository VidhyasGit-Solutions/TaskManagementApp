from flask import Flask
runserver = Flask(__name__, static_folder='static')

import UserLogin.views