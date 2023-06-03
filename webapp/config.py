from os import environ, path
import os
from dotenv import load_dotenv

# Specificy a `.env` file containing key/value config values
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    # General Config
    #SECRET_KEY = environ.get("SECRET_KEY")
    SECRET_KEY = os.urandom(32)
 
    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    #SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:1111@localhost/test'
