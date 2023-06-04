from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.Config')
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# testing smaller database
# from . import dump_testing
# dump_testing.dump_db() 

from . import routes, models