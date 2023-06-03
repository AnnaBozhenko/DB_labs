from sqlalchemy import MetaData, Table, insert, select, func, delete, desc, ForeignKey

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
                   "avg": func.avg(Test.c.ball100)}

def insert_into_locationInfo():
    pass

def get_locationinfo():
    with engine.connect() as conn:
        query_locations = select(LocationInfo).order_by(desc(LocationInfo.c.locationid))
        locations = conn.execute(query_locations).all()
    return locations

def delete_location(location_id):
    with engine.connect() as conn:
        query = LocationInfo.delete().where(LocationInfo.c.locationid == location_id)
        conn.execute(query)
        conn.commit()


def get_institution():
    with engine.connect() as conn:
        query_institution = select(Institution).order_by(desc(Institution.c.instid))
        institutions = conn.execute(query_institution).all()
    return institutions

def delete_institution(inst_Id):
    with engine.connect() as conn:
        query = Institution.delete().where(Institution.c.instid == inst_Id)
        conn.execute(query)
        conn.commit()

def get_student():
    with engine.connect() as conn:
        query_student = select(Student)
        students = conn.execute(query_student).all()
    return students


def delete_student(out_id):
    with engine.connect() as conn:
        query = Student.delete().where(Student.c.outid == out_id)
        conn.execute(query)
        conn.commit()


def get_test():
    with engine.connect() as conn:
        query_test = select(Test).order_by(desc(Test.c.testid))
        tests = conn.execute(query_test).all()
    return tests


def delete_test(test_Id):
    with engine.connect() as conn:
        query = Test.delete().where(Test.c.testid == test_Id)
        conn.execute(query)
        conn.commit()

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

# def get_locationinfo():
#     result = None
#     with engine.connect() as conn:
#         result = conn.execute(select(LocationInfo).order_by(desc(LocationInfo.c.locationid))).all()
#     return result
#
# def get_institution():
#     result = None
#     with engine.connect() as conn:
#         result = conn.execute(select(Institution).order_by(desc(Institution.c.instid))).all()
#     return result
#
# def get_test():
#     result = None
#     with engine.connect() as conn:
#         result = conn.execute(select(Test)).all()
#     return result
#
# def get_student():
#     result = None
#     with engine.connect() as conn:
#         result = conn.execute(select(Student)).all()
#     return result


# def delete_location(value):
#     with engine.connect() as conn:
#         conn.execute(delete(LocationInfo).where(LocationInfo.c.locationid == value))
#         conn.commit()
#
# def delete_institution(value):
#     with engine.connect() as conn:
#         conn.execute(delete(LocationInfo).where(LocationInfo.c.locationid == value))
#         conn.commit()
    

def insert_location(values):
    with engine.connect() as conn:
        # check if exists
        check_query = select(LocationInfo).where(LocationInfo.c.areaname == values['areaname'],
                                                 LocationInfo.c.regname == values['regname'],
                                                 LocationInfo.c.tername == values['tername'])
        if not conn.execute(check_query).all():
            conn.execute(insert(LocationInfo), values)
            conn.commit()


def insert_institution(values):
    with engine.connect() as conn:
        # check if exists
        check_query = select(Institution).where(Institution.c.instname == values['instname'],
                                                Institution.c.locationid == values['locationid'])
        if not conn.execute(check_query).all():
            conn.execute(insert(Institution), values)
            conn.commit()


def insert_student(values):
    with engine.connect() as conn:
        check_query = select(Student).where(Student.c.outid == values['outid'])
        if not conn.execute(check_query).all():
            conn.execute(insert(Student), values)
            conn.commit()


def insert_test(values):
    with engine.connect() as conn:
        values['subtest'] = True if values['subtest'].lower() == 'так' else False
        conn.execute(insert(Test), values)
        conn.commit()


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
    # insert to locations
    student_location = {'areaname': values['student_area'], 
                        'regname': values['student_region'], 
                        'tername': values['student_ter']}
    insert_location(student_location)

    student_inst_location = {'areaname': values['student_inst_area'],
                            'regname': values['student_inst_region'],
                            'tername': values['student_inst_ter']}
    insert_location(student_inst_location)
    
    test_inst_location =    {'areaname': values['test_inst_area'],
                            'regname': values['test_inst_region'],
                            'tername': values['test_inst_ter']}
    insert_location(test_inst_location)
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
    test_institution = {'instname': values['test_inst_name'],
                        'locationid': test_inst_location_id,
                        'insttype': None,
                        'instparent': None}
    insert_institution(test_institution)

    stud_institution = {'instname': values['student_inst_name'],
                        'locationid': stud_inst_location_id,
                        'insttype': values['student_inst_type'],
                        'instparent': values['student_inst_parent']}
    insert_institution(stud_institution)
    
    with engine.connect() as conn:
        stud_inst_id = conn.execute(select(Institution.c.instid). \
                                           join_from(Institution, LocationInfo). \
                                           where(LocationInfo.c.locationid == stud_inst_location_id)).first()[0]
        
        test_inst_id = conn.execute(select(Institution.c.instid). \
                                           join_from(Institution, LocationInfo). \
                                           where(LocationInfo.c.locationid == test_inst_location_id)).first()[0]
        
    # insert to student
    student = {'outid': values['student_id'],
                'birth': values['student_birth'],
                'sextypename': values['student_sex'],
                'locationid': stud_location_id,
                'regtypename': values['student_regtype'],
                'classprofilename': values['class_profile'],
                'classlangname': values['class_lang'],
                'instid': stud_inst_id}
    insert_student(student)
    # insert to test
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
    insert_test(test)
