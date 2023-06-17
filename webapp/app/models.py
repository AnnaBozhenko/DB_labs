from sqlalchemy import MetaData, Table, insert, select, update, func, delete, desc, ForeignKey
import redis
from time import perf_counter
import functools
from . import engine
# from hashlib import sha224

redis_url = 'redis://redis:6379/0'
redisClient = redis.from_url(redis_url)
CACHELIFETIME = 300
#  ---- TABLES MAPPING -----
metadata_obj = MetaData()
LocationInfo = Table("locationinfo", metadata_obj, autoload_with=engine, schema="public")
Institution = Table("institution", metadata_obj, autoload_with=engine, schema="public")
Student = Table("student", metadata_obj, autoload_with=engine, schema="public")
Test = Table("test", metadata_obj, autoload_with=engine, schema="public")
statistic_funcs = {"min": func.min(Test.c.ball100),
                   "max": func.max(Test.c.ball100),
                   "avg": func.avg(Test.c.ball100)}

def timer(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__!r} in {(perf_counter() - start_time):.4f} seconds")
        return result
    return inner


class PGLocationInfo:
    def insert(cls, values):
        with engine.connect() as conn:
            check_query = select(LocationInfo).where(LocationInfo.c.areaname == values['areaname'],
                                                     LocationInfo.c.regname == values['regname'],
                                                     LocationInfo.c.tername == values['tername'])
            if not conn.execute(check_query).first():
                conn.execute(insert(LocationInfo), values)
                conn.commit()


    def update(cls, row_to_update):
        with engine.connect() as conn:
            location = conn.execute(select(LocationInfo).where(LocationInfo.c.locationid == row_to_update["locationid"])).first()
            if location:
                areaname, regname, tername, id = location
                if row_to_update['areaname']:
                    areaname = row_to_update['areaname']
                if row_to_update['regname']:
                    regname = row_to_update['regname']
                if row_to_update['tername']:
                    tername = row_to_update['tername']
                q = update(LocationInfo).where(LocationInfo.c.locationid == id).values(areaname=areaname, regname=regname, tername=tername)
                conn.execute(q)
                conn.commit()


    def delete(cls, location_id):
        with engine.connect() as conn:
            # delete dependant structures
            query = delete(Test).where(Test.c.instid == Institution.c.instid, Institution.c.locationid == LocationInfo.c.locationid, LocationInfo.c.locationid == location_id)
            conn.execute(query)
            query = delete(Student).where(Student.c.instid == Institution.c.instid, Institution.c.locationid == LocationInfo.c.locationid, LocationInfo.c.locationid == location_id)
            conn.execute(query)
            query = delete(Institution).where(Institution.c.locationid == location_id)
            conn.execute(query)
            query = delete(LocationInfo).where(LocationInfo.c.locationid == location_id)
            conn.execute(query)
            conn.commit()

    def info(cls):
        with engine.connect() as conn:
            query_locations = select(LocationInfo).order_by(desc(LocationInfo.c.locationid))
            locations = conn.execute(query_locations).all()
        return locations
    

class PGInstitution:
    def insert(cls, values):
        with engine.connect() as conn:
            check_query = select(Institution).where(Institution.c.instname == values['instname'],
                                                    Institution.c.locationid == values['locationid'])
            if not conn.execute(check_query).first():
                conn.execute(insert(Institution), values)
                conn.commit()


    def update(cls, row_to_update):
        valid_to_update = True
        with engine.connect() as conn:
            institution = conn.execute(select(Institution).where(Institution.c.instid == row_to_update["instid"])).first()
            if institution:
                instname, locationid, insttype, instparent, instid = institution
                if row_to_update['instname']:
                    instname = row_to_update['instname']
                if row_to_update['locationid']:
                    locationid = row_to_update['locationid']
                    if not conn.execute(select(LocationInfo).where(LocationInfo.c.locationid == locationid)).first():
                        valid_to_update = False
                if row_to_update['insttype']:
                    insttype = row_to_update['insttype']
                if row_to_update['instparent']:
                    instparent = row_to_update['instparent']
                if valid_to_update:
                    conn.execute(update(Institution) \
                                 .where(Institution.c.instid == instid) \
                                 .values(instname=instname, 
                                         locationid = locationid,
                                         insttype=insttype,
                                         instparent=instparent))
                    conn.commit()


    def delete(cls, inst_Id):
        with engine.connect() as conn:
            query = delete(Test).where(Test.c.outid == Student.c.outid, Student.c.instid == inst_Id)
            conn.execute(query)
            query = delete(Student).where(Student.c.instid == inst_Id)
            conn.execute(query)
            query = delete(Test).where(Test.c.instid == inst_Id)
            conn.execute(query)
            query = delete(Institution).where(Institution.c.instid == inst_Id)
            conn.execute(query)
            conn.commit()

    def info(cls):
        with engine.connect() as conn:
            query_institution = select(Institution).order_by(desc(Institution.c.instid))
            institutions = conn.execute(query_institution).all()
        return institutions
    

class PGStudent:
    def insert(cls, values):
        with engine.connect() as conn:
            check_query = select(Student).where(Student.c.outid == values['outid'])
            if not conn.execute(check_query).first():
                conn.execute(insert(Student), values)
                conn.commit()

    def update(cls, row_to_update):
        valid_to_update = True
        with engine.connect() as conn:
            student = conn.execute(select(Student).where(Student.c.outid == row_to_update["outid"])).first()
            if student:
                outid, birth, sextypename, locationid, regtypename, classprofilename, classlangname, instid = student
                if row_to_update['birth']:
                    birth = row_to_update['birth']
                if row_to_update['sextypename']:
                    sextypename = row_to_update['sextypename']
                if row_to_update['regtypename']:
                    regtypename = row_to_update['regtypename']
                if row_to_update['classprofilename']:
                    classprofilename = row_to_update['classprofilename']
                if row_to_update['classlangname']:
                    classlangname = row_to_update['classlangname']
                if row_to_update['locationid']:
                    locationid = row_to_update['locationid']
                    if not conn.execute(select(LocationInfo).where(LocationInfo.c.locationid == locationid)).first():
                        valid_to_update = False
                if row_to_update['instid']:
                    instid = row_to_update['instid']
                    if not conn.execute(select(Institution).where(Institution.c.instid == instid)).first():
                        valid_to_update = False
                if valid_to_update:
                    conn.execute(update(Student) \
                                 .where(Student.c.outid == outid) \
                                 .values(birth=birth,
                                         sextypename=sextypename,
                                         locationid=locationid,
                                         regtypename=regtypename,
                                         classprofilename=classprofilename,
                                         classlangname=classlangname,
                                         instid=instid))
                    conn.commit()

    def delete(cls, out_id):
        with engine.connect() as conn:
            query = delete(Test).where(Test.c.outid == out_id)
            conn.execute(query)
            query = delete(Student).where(Student.c.outid == out_id)
            conn.execute(query)
            conn.commit()

    def info(cls):
        with engine.connect() as conn:
            query_student = select(Student)
            students = conn.execute(query_student).all()
        return students


class PGTest:
    def insert(cls, values):
        with engine.connect() as conn:
            conn.execute(insert(Test), values)
            conn.commit()

    def update(cls, row_to_update):
        valid_to_update = True
        with engine.connect() as conn:
            test = conn.execute(select(Test).where(Test.c.testid == row_to_update["testid"])).first()
            if test:
                instid, testyear, adaptscale, ball12, ball100, ball, subtest, outid, testname, dpalevel, testlang, teststatus, testid = test
                if row_to_update['testyear']:
                    testyear = row_to_update['testyear']
                if row_to_update['adaptscale']:
                    adaptscale = row_to_update['adaptscale']
                if row_to_update['ball12']:
                    ball12 = row_to_update['ball12']
                if row_to_update['ball100']:
                    ball100 = row_to_update['ball100']
                if row_to_update['ball']:
                    ball = row_to_update['ball']
                if row_to_update['subtest']:
                    subtest = row_to_update['subtest']
                if row_to_update['testname']:
                    testname = row_to_update['testname']
                if row_to_update['dpalevel']:
                    dpalevel = row_to_update['dpalevel']
                if row_to_update['testlang']:
                    testlang = row_to_update['testlang']
                if row_to_update['teststatus']:
                    teststatus = row_to_update['teststatus']
                if row_to_update['outid']:
                    outid = row_to_update['outid']
                    if not conn.execute(select(Student).where(Student.c.outid == outid)).first():
                        valid_to_update = False
                if row_to_update['instid']:
                    instid = row_to_update['instid']
                    if not conn.execute(select(Institution).where(Institution.c.instid == instid)).first():
                        valid_to_update = False
                if valid_to_update:
                    conn.execute(update(Test) \
                                 .where(Test.c.testid == testid) \
                                 .values(instid=instid, 
                                         testyear=testyear, 
                                         adaptscale=adaptscale, 
                                         ball12=ball12, 
                                         ball100=ball100, 
                                         ball=ball, 
                                         subtest=subtest, 
                                         outid=outid, 
                                         testname=testname, 
                                         dpalevel=dpalevel, 
                                         testlang=testlang, 
                                         teststatus=teststatus))
                    conn.commit()    

    def delete(cls, test_Id):
        with engine.connect() as conn:
            query = delete(Test).where(Test.c.testid == test_Id)
            conn.execute(query)
            conn.commit()

    def info(cls):
        with engine.connect() as conn:
            query_test = select(Test).order_by(desc(Test.c.testid))
            tests = conn.execute(query_test).all()
        return tests


@timer
def get_statistics(years, regions, subjects, ball_function, teststatus):
    """give statistics on query with given years, regin names subjects, 
    ball_function (min/max/average), teststatus(зараховано/не зараховано)"""
    result = []
    uncached_combinations = []
    for year in years:
        for region in regions:
            key = f"{year}_{region}_{ball_function}"
            # key = sha224(key.encode()).hexdigest()
            ball = redisClient.get(key)
            if ball is not None:
                result.append((year, region, float(ball)))
            else:
                uncached_combinations.append((year, region))

    if result:
        print("cache retrieved")
    if uncached_combinations:
        with engine.connect() as conn:
            for constraint in uncached_combinations:
                query = select(Test.c.testyear, LocationInfo.c.regname, func.round(statistic_funcs[ball_function], 2)) \
                        .where(Test.c.instid == Institution.c.instid, Institution.c.locationid == LocationInfo.c.locationid) \
                        .where(Test.c.testyear == constraint[0], 
                               LocationInfo.c.regname == constraint[1], 
                               Test.c.testname.in_(subjects), 
                               Test.c.teststatus == teststatus) \
                        .group_by(LocationInfo.c.regname, Test.c.testyear)
                statistics = conn.execute(query).all()
                print("result:")
                [print(s) for s in statistics]
                for s in statistics:
                    # write to cache
                    key = f"{s[0]}_{s[1]}_{ball_function}"
                    # key = sha224(key.encode()).hexdigest()
                    ball = float(s[2])
                    redisClient.set(name=key, value=ball, ex=CACHELIFETIME)
                    result.append(s)
    return result
                

def insert_data(values):
    """
    {'student_id'
    'student_birth'
    'student_sex'
    'student_area'
    'student_region'
    'student_ter'
    'student_regtype'
    'class_profile'
    'class_lang'
    'student_inst_name'
    'student_inst_area'
    'student_inst_region'
    'student_inst_ter'
    'student_inst_type'
    'student_inst_parent'

    'test_name'
    'test_inst_name'
    'test_inst_area'
    'test_inst_region'
    'test_inst_ter'
    'test_year'
    'adapt_scale'
    'ball12'
    'ball100'
    'ball'
    'subtest'
    'dpalevel'
    'test_lang'
    'test_status'}
    """
    locations = PGLocationInfo()
    # insert to locations
    student_location = {'areaname': values['student_area'], 
                        'regname': values['student_region'], 
                        'tername': values['student_ter']}
    locations.insert(student_location)

    student_inst_location = {'areaname': values['student_inst_area'],
                            'regname': values['student_inst_region'],
                            'tername': values['student_inst_ter']}
    locations.insert(student_inst_location)
    
    test_inst_location =    {'areaname': values['test_inst_area'],
                            'regname': values['test_inst_region'],
                            'tername': values['test_inst_ter']}
    locations.insert(test_inst_location)
    # get locations id
    with engine.connect() as conn:
        stud_location_id = conn.execute(select(LocationInfo.c.locationid). \
                           where(LocationInfo.c.areaname == values['student_area'],
                                 LocationInfo.c.tername == values['student_ter'],
                                 LocationInfo.c.regname == values['student_region'])).first()[0]
        
        stud_inst_location_id = conn.execute(select(LocationInfo.c.locationid). \
                                where(LocationInfo.c.areaname == values['student_inst_area'],  
                                      LocationInfo.c.tername ==       values['student_inst_ter'],
                                      LocationInfo.c.regname ==       values['student_inst_region'])).first()[0]
        
        test_inst_location_id = conn.execute(select(LocationInfo.c.locationid). \
                                where(LocationInfo.c.areaname == values['test_inst_area'],  
                                      LocationInfo.c.tername ==       values['test_inst_ter'],
                                      LocationInfo.c.regname ==       values['test_inst_region'])).first()[0]
    # insert institutions
    institutions = PGInstitution()
    test_institution = {'instname': values['test_inst_name'],
                        'locationid': test_inst_location_id,
                        'insttype': None,
                        'instparent': None}
    institutions.insert(test_institution)

    stud_institution = {'instname': values['student_inst_name'],
                        'locationid': stud_inst_location_id,
                        'insttype': values['student_inst_type'],
                        'instparent': values['student_inst_parent']}
    institutions.insert(stud_institution)
    
    with engine.connect() as conn:
        stud_inst_id = conn.execute(select(Institution.c.instid). \
                                           join_from(Institution, LocationInfo). \
                                           where(LocationInfo.c.locationid == stud_inst_location_id)).first()[0]
        
        test_inst_id = conn.execute(select(Institution.c.instid). \
                                           join_from(Institution, LocationInfo). \
                                           where(LocationInfo.c.locationid == test_inst_location_id)).first()[0]
        
    # insert to student
    students = PGStudent()
    student = {'outid': values['student_id'],
                'birth': values['student_birth'],
                'sextypename': values['student_sex'],
                'locationid': stud_location_id,
                'regtypename': values['student_regtype'],
                'classprofilename': values['class_profile'],
                'classlangname': values['class_lang'],
                'instid': stud_inst_id}
    students.insert(student)
    # insert to test
    tests = PGTest()
    test = {'instid': test_inst_id,
            'testyear': values['test_year'],
            'outid': values['student_id'],
            'adaptscale': values['adapt_scale'],
            'ball12': values['ball12'],
            'ball100': values['ball100'],
            'ball': values['ball'],
            'subtest': values['subtest'],
            'dpalevel': values['dpalevel'],
            'testlang': values['test_lang'],
            'teststatus': values['test_status']}
    tests.insert(test)
