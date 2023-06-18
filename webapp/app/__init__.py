from flask import Flask
from sqlalchemy import create_engine

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.Config')
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
DB = app.config['DB']
# engine = create_engine("postgresql+psycopg2://postgres:turtle@localhost/python_db")

# testing smaller database
from . import dump_testing
dump_testing.dump_db() 
if DB == "MONGO":
    from . import mongo_logics
    mongo_logics.run_migrations()
    locations = mongo_logics.MongoLocationInfo()
    institutions = mongo_logics.MongoInstitution()
    students = mongo_logics.MongoStudent()
    tests = mongo_logics.MongoTest()
else:
    from . import models
    locations = models.PGLocationInfo()
    institutions = models.PGInstitution()
    students = models.PGStudent()
    tests = models.PGTest()    

from . import routes

