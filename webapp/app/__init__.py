from flask import Flask
from sqlalchemy import create_engine

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.Config')
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
# engine = create_engine("postgresql+psycopg2://postgres:turtle@localhost/python_db")

# testing smaller database
from . import dump_testing
dump_testing.dump_db() 
from . import mongo_logics
mongo_logics.run_migrations()

from . import routes, models

