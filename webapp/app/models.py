from sqlalchemy import MetaData, Table
from . import engine

metadata_obj = MetaData()

LocationInfo = Table("locationinfo", metadata_obj, autoload_with=engine, schema="public")
Institution = Table("institution", metadata_obj, autoload_with=engine, schema="public")
Student = Table("student", metadata_obj, autoload_with=engine, schema="public")
Test = Table("test", metadata_obj, autoload_with=engine, schema="public")
