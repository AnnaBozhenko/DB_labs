from sqlalchemy import MetaData, Table, select, func
from . import engine

#  ---- TABLES MAPPING -----
metadata_obj = MetaData()

LocationInfo = Table("locationinfo", metadata_obj, autoload_with=engine, schema="public")
Institution = Table("institution", metadata_obj, autoload_with=engine, schema="public")
Student = Table("student", metadata_obj, autoload_with=engine, schema="public")
Test = Table("test", metadata_obj, autoload_with=engine, schema="public")
# -------------------------
statistic_funcs = {"min": func.min(Test.c.ball100),
                   "max": func.max(Test.c.ball100),
                   "avg": func.avg(Test.c.ball100),
                   "plain": Test.c.ball100}

def get_statistics(years, regions, subjects, ball_function, teststatus):
    """give statistics on query with given years, regin names subjects, 
    ball_function (min/max/average/plain - no function to apply), teststatus(зараховано/не зараховано)"""
    constraints = []
    if years:
        constraints.append(Test.c.testyear.in_(years))
    if regions:
        constraints.append(LocationInfo.c.regname.in_(regions))
    if subjects:
        constraints.append(Test.c.testname.in_(subjects))
    if teststatus:
        constraints.append(Test.c.teststatus == teststatus)
    query = None
    if ball_function == "plain":
        query = select(Test.c.testyear, LocationInfo.c.regname, Test.c.testname, Test.c.ball100) \
                .where(Test.c.instid == Institution.c.instid, Institution.c.locationid == LocationInfo.c.locationid) \
                .where(*constraints)
    else:
        query = select(Test.c.testyear, LocationInfo.c.regname, Test.c.testname, statistic_funcs[ball_function]) \
                .where(Test.c.instid == Institution.c.instid, Institution.c.locationid == LocationInfo.c.locationid) \
                .where(*constraints) \
                .group_by(Test.c.testyear, LocationInfo.c.regname, Test.c.testname)    
    result = None        
    with engine.connect() as conn:
        result = conn.execute(query).all()
    return result
