from app import app, engine
#from webapp.app.models import LocationInfo, Institution, Student, Test
from sqlalchemy import bindparam, insert, select
from flask import Flask, render_template

app = Flask(__name__)

def insert_into_locationInfo(values):
    """values - list of dictionaries e.g [{'areaName': x, 'terName': y, 'regName': z}]"""
    if values:
        with engine.connect() as conn:
            conn.execute(insert(LocationInfo).values(areaName = 'areaName', terName = 'terName', regName = 'regName'), values,)
            conn.commit()


def insert_into_institution(values):
    """values - list of dictionaries e.g. [{'instName': , 'instType': , 'instParent': , 'areaName': , 'terName': , 'regName': }]"""
    if values:
    # check if location info about institution is present in LocationInfo table, if not - insert into location_info such info
        with engine.connect() as conn:
            locations_to_insert = []
            for row in values:
                subq = select(LocationInfo.c.id).where(LocationInfo.c.areaName == row['areaName'] and
                                                       LocationInfo.c.terName == row['terName'] and
                                                       LocationInfo.c.regName == row['regName'])
                if not [row for row in conn.execute(subq)]:
                    locations_to_insert.append({row['areaName'], row['terName'], row['regName']}) 
            insert_into_locationInfo(locations_to_insert)
    # perform insertion
        with engine.connect() as conn:
            select_locationId = select(LocationInfo.c.locationId).where(LocationInfo.c.areaName == bindparam('areaName') and 
                                                                   LocationInfo.c.terName == bindparam('terName') and 
                                                                   LocationInfo.c.regName == bindparam('regName'))
            conn.execute(insert(Institution).values(locationId = select_locationId, 
                                                    instName = 'instName',
                                                    instType = 'instType',
                                                    instParent = 'instParent'), values,)
            conn.commit()


def insert_into_student(values):
    """values - list of dictionaries e.g. [{'outId': , 'birth': , 'sexTypeName': , 'regTypeName', 'areaName': , 'terName': , 'regName': , 'classProfileName', 'classLangName', 'eoName', 'eoAreaName', 'eoRegName', 'eoTerName'}]"""
    if values:
        locations_to_insert = []
    # check if location info about student and sdudent's institution are present in LocationInfo table, if not - insert into location_info such info
        with engine.connect() as conn:
            for row in values:
            # check student's location
                subq = select(LocationInfo.c.id).where(LocationInfo.c.areaName == row['areaName'] and
                                                       LocationInfo.c.terName == row['terName'] and
                                                       LocationInfo.c.regName == row['regName'])
                if not [row for row in conn.execute(subq)]:
                    locations_to_insert.append({row['areaName'], row['terName'], row['regName']})
            # check student's institution location
                subq = select(LocationInfo.c.id).where(LocationInfo.c.areaName == row['eoAreaName'] and
                                                       LocationInfo.c.terName == row['eoTerName'] and
                                                       LocationInfo.c.regName == row['eoRegName'])
                if not [row for row in conn.execute(subq)]:
                    locations_to_insert.append({row['eoAreaName'], row['eoTerName'], row['eoRegName']})
        insert_into_locationInfo(locations_to_insert)
    # perform insertion
        with engine.connect() as conn:
            select_stud_locationId = select(LocationInfo.c.locationId).where(LocationInfo.c.areaName == bindparam('areaName') and 
                                                                   LocationInfo.c.terName == bindparam('terName') and 
                                                                   LocationInfo.c.regName == bindparam('regName'))
            
            # select_inst_locationId = select(LocationInfo.c.locationId).where(LocationInfo.c.areaName == bindparam('eoAreaName') and 
            #                                                        LocationInfo.c.terName == bindparam('eoTerName') and 
            #                                                        LocationInfo.c.regName == bindparam('eoRegName'))
            
            conn.execute(insert(Student).values(outId = 'outId',
                                                birth = 'birth',
                                                sexTypeName = 'sexTypeName',
                                                locationId = select_stud_locationId, 
                                                regTypeName = 'regTypeName',
                                                classProfileName = 'classProfileName',
                                                classLangName = 'classLangName',
                                                institutionId = ''), values,)
            conn.commit()


def insert_into_test(values):
    pass


@app.shell_context_processor
def make_shell_context():
    return {'LocationInfo': LocationInfo, 'Institution': Institution, 'Student': Student, 'Test': Test}

# @app.route('/', methods=['GET', 'POST'])
# def main_page():
#     return render_template('index.html')
#
# @app.route('/location_info/', methods=['GET', 'POST'])
# def location_info():
#     return render_template('location.html')
#
#
# @app.route('/institution_info/', methods=['GET', 'POST'])
# def institution_info():
#     return render_template('institution.html')
#
#
# @app.route('/student_info/', methods=['GET', 'POST'])
# def student_info():
#     return render_template('student.html')
#
#
# @app.route('/test_info/', methods=['GET', 'POST'])
# def test_info():
#     return render_template('test.html')
#
#
# @app.route('/queries_info/', methods=['GET', 'POST'])
# def queries():
#     return render_template("queries.html", title="Queries")
#
#
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", debug=True)

