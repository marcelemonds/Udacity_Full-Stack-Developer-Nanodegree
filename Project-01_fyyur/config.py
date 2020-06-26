import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

class Config(object):
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:1234@localhost:5432/fyyur'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
