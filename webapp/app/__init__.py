import functools
from time import perf_counter
from flask import Flask
from sqlalchemy import create_engine
import redis

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.Config')
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
DB = app.config['DB']
redis_url = 'redis://redis:6379/0'
redisClient = redis.from_url(redis_url)
CACHELIFETIME = 300
# engine = create_engine("postgresql+psycopg2://postgres:turtle@localhost/python_db")

# testing smaller database
# from . import dump_testing
# dump_testing.dump_db() 


if DB == "MONGO":
    from . import mongo_logics
    mongo_logics.run_migrations()
    locations = mongo_logics.MongoLocationInfo()
    institutions = mongo_logics.MongoInstitution()
    students = mongo_logics.MongoStudent()
    tests = mongo_logics.MongoTest()
    get_statistics = mongo_logics.get_statistics
else:
    from . import models
    locations = models.PGLocationInfo()
    institutions = models.PGInstitution()
    students = models.PGStudent()
    tests = models.PGTest()    
    get_statistics = models.get_statistics


def timer(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__!r} in {(perf_counter() - start_time):.4f} seconds")
        return result
    return inner


@timer
def get_multiple_statistics(years, regions, subject, ball_function, teststatus):
    """give statistics on query with given years, region names, subject, 
    ball_function (min/max/average), teststatus(зараховано/не зараховано)"""
    result = []
    uncached_combinations = []
    for year in years:
        for region in regions:
            key = f"{subject}_{year}_{region}_{ball_function}"
            # key = sha224(key.encode()).hexdigest()
            ball = redisClient.get(key)
            if ball is not None:
                result.append((year, region, float(ball)))
            else:
                uncached_combinations.append({"subject": subject, "regname": region, "testyear": year, "teststatus": teststatus, "ball_function": ball_function})

    if result:
        print("cache retrieved")
    if uncached_combinations:
        for constraint in uncached_combinations:
            statistics = get_statistics(constraint)
            for s in statistics:
                # write to cache
                key = f"{subject}_{s[0]}_{s[1]}_{ball_function}"
                # key = sha224(key.encode()).hexdigest()
                ball = float(s[2])
                redisClient.set(name=key, value=ball, ex=CACHELIFETIME)
                result.append(s)
    print("result:")
    [print(x) for x in result]
    return result

from . import routes
