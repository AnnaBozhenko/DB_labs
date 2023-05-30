from app import app, engine
from app.models import LocationInfo, Institution, Student, Test
from sqlalchemy import bindparam, insert, select
from flask import Flask, render_template

app = Flask(__name__)

def insert_into_locationInfo(values):
    """values - list of dictionaries e.g [{'areaname': x, 'tername': y, 'regname': z}]"""
    if values:
        with engine.connect() as conn:
            conn.execute(insert(LocationInfo).values(areaname = 'areaname', tername = 'tername', regname = 'regname'), values,)
            conn.commit()


def insert_into_institution(values):
    """values - list of dictionaries e.g. [{'instname': , 'insttype': , 'instparent': , 'areaname': , 'tername': , 'regname': }]"""
    if values:
    # check if location info about institution is present in LocationInfo table, if not - insert into location_info such info
        with engine.connect() as conn:
            locations_to_insert = []
            for row in values:
                subq = select(LocationInfo.c.id).where(LocationInfo.c.areaname == row['areaname'] and
                                                       LocationInfo.c.tername == row['tername'] and
                                                       LocationInfo.c.regname == row['regname'])
                if not [row for row in conn.execute(subq)]:
                    locations_to_insert.append({row['areaname'], row['tername'], row['regname']}) 
            insert_into_locationInfo(locations_to_insert)
    # perform insertion
        with engine.connect() as conn:
            select_locationid = select(LocationInfo.c.locationid).where(LocationInfo.c.areaname == bindparam('areaname') and 
                                                                   LocationInfo.c.tername == bindparam('tername') and 
                                                                   LocationInfo.c.regname == bindparam('regname'))
            conn.execute(insert(Institution).values(locationid = select_locationid, 
                                                    instname = 'instname',
                                                    insttype = 'insttype',
                                                    instparent = 'instparent'), values,)
            conn.commit()


def insert_into_student(values):
    """values - list of dictionaries e.g. [{'outId': , 'birth': , 'sextypename': , 'regtypename', 'areaname': , 'tername': , 'regname': , 'classprofilename', 'classlangname', 'eoName', 'eoareaname', 'eoregname', 'eotername'}]"""
    if values:
        locations_to_insert = []
    # check if location info about student and sdudent's institution are present in LocationInfo table, if not - insert into location_info such info
        with engine.connect() as conn:
            for row in values:
            # check student's location
                subq = select(LocationInfo.c.id).where(LocationInfo.c.areaname == row['areaname'] and
                                                       LocationInfo.c.tername == row['tername'] and
                                                       LocationInfo.c.regname == row['regname'])
                if not [row for row in conn.execute(subq)]:
                    locations_to_insert.append({row['areaname'], row['tername'], row['regname']})
            # check student's institution location
                subq = select(LocationInfo.c.id).where(LocationInfo.c.areaname == row['eoareaname'] and
                                                       LocationInfo.c.tername == row['eotername'] and
                                                       LocationInfo.c.regname == row['eoregname'])
                if not [row for row in conn.execute(subq)]:
                    locations_to_insert.append({row['eoareaname'], row['eotername'], row['eoregname']})
        insert_into_locationInfo(locations_to_insert)
    # perform insertion
        with engine.connect() as conn:
            select_stud_locationid = select(LocationInfo.c.locationid).where(LocationInfo.c.areaname == bindparam('areaname') and 
                                                                   LocationInfo.c.tername == bindparam('tername') and 
                                                                   LocationInfo.c.regname == bindparam('regname'))
            
            # select_inst_locationid = select(LocationInfo.c.locationid).where(LocationInfo.c.areaname == bindparam('eoareaname') and 
            #                                                        LocationInfo.c.tername == bindparam('eotername') and 
            #                                                        LocationInfo.c.regname == bindparam('eoregname'))
            
            conn.execute(insert(Student).values(outId = 'outId',
                                                birth = 'birth',
                                                sextypename = 'sextypename',
                                                locationid = select_stud_locationid, 
                                                regtypename = 'regtypename',
                                                classprofilename = 'classprofilename',
                                                classlangname = 'classlangname',
                                                institutionid = ''), values,)
            conn.commit()


def insert_into_test(values):
    pass


@app.shell_context_processor
def make_shell_context():
    return {'LocationInfo': LocationInfo, 'Institution': Institution, 'Student': Student, 'Test': Test}

