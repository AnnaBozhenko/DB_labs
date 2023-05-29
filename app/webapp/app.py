from app import app



# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine

# Base = automap_base()

# engine = create_engine('postgresql+psycopg2://user:password@host/database_name')

# # reflect the tables
# Base.prepare(autoload_with=engine)

# LocationInfo = Base.classes.locationinfo
# Institution = Base.classes.institution
# Student = Base.classes.student
# Test = Base.classes.test


# #session = Session(engine)
# with Session(engine) as session:
#     pass
#     session.commit()