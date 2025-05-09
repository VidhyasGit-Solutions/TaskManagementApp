import os
from UserLogin import runserver    # Imports the code from UserLogin/__init__.py

if __name__ == '__main__':
    HOST = os.environ.get('SERVER_HOST', 'localhost')

    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    runserver.run(HOST, PORT)