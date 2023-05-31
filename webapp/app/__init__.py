from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.Config')
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


# def db_session(func):
#     def inner(*args, **kwargs):
#         with Session(engine) as session:
#             func_call = func(*args, **kwargs)
#             session.commit()
#             return func_call
#     return inner

from . import routes, models