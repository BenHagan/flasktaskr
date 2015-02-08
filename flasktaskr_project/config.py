# config.py

import os

# grabs the folder where the script runs

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'my_precious'
DEBUG = False
#PROPAGATE_EXCEPTIONS = True

# defines the full path for the DATABASE
DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH