from flask import Flask
import secrets

runserver = Flask(__name__, static_folder='static')
# Generate a secure secret key
secret_key = secrets.token_hex(16)
runserver.secret_key = secret_key

import UserLogin.views