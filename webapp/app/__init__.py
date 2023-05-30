from flask import Flask
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


app = Flask(__name__)
app.config.from_object('config')
app.config.from_object(Config)

# prepare database connection
engine = create_engine('postgresql+psycopg2://postgres:turtle@localhost/python_db')
 
def db_session(func):
    def inner(*args, **kwargs):
        with Session(engine) as session:
            func_call = func(*args, **kwargs)
            session.commit()
            return func_call
    return inner

from app import routes