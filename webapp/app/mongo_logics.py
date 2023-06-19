import psycopg2 as pg
import pymongo

POSTGRES_DB = "ZNO"
POSTGRES_USER= "Student"
POSTGRES_PASSWORD = "qwerty"
POSTGRES_HOST = "db"
chunk = 100
client = pymongo.MongoClient("mongodb://user:pass@mongodb:27017/")
mongo_db = client["ZNO"]

query_locationinfo = """
select row_to_json(l)
from 
(select 
 	locationid,
 	areaname,
    regname,
    tername
 from locationinfo
) l"""

query_institution = """
select row_to_json(i)
from 
(select 
 	instid,
 	instname,
    insttype,
    instparent,
    locationid
from institution) i;"""

query_student = """
select row_to_json(s)
from 
(select
    outid,
    birth,
    sextypename,
    locationid,
    regtypename,
    classprofilename,
    classlangname,
    instid
from student) s;"""

query_test = """
select row_to_json(t)
from 
(select 
    testid,
    instid,
    testyear,
    adaptscale,
    ball12,
    ball100,
    ball,
    subtest,
    outid,
    testname,
    dpalevel,
    testlang,
    teststatus
from test) t;"""

def migrate(query, collection_name):
    conn = None
    try:
        conn = pg.connect(dbname=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST)
        with conn.cursor() as cur:
            collections = mongo_db[collection_name]
            cur.execute(query)
            results = [el[0] for el in cur.fetchall()]
            i = 0
            while i < len(results):
                collections.insert_many(results[i: i+chunk])
                i += chunk 
    except pg.OperationalError:
        pass
    except Exception:
        pass
    finally:
        if conn:
            print("Table was migrated to collection")
            conn.close()


def get_valid_fields(dictionary):
    valid_dictionary = dict()
    for key, value in dictionary.items():
        if value:
            valid_dictionary[key] = value
    return valid_dictionary

class MongoLocationInfo:
    def __init__(cls):
        cls.validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["locationid"],
                "properties": {
                    "locationid": {
                        "bsonType": "int"
                    },
                    "areaname": {
                        "bsonType": ["string", "null"]
                    },
                    "tername": {
                        "bsonType": ["string", "null"]
                    },
                    "regname": {
                        "bsonType": ["string", "null"]
                    },
                }
            }
        }
        if "collLocationInfo" not in mongo_db.list_collection_names():  
            cls.col = mongo_db.create_collection('collLocationInfo', validator=cls.validator, validationAction="error")
            cls.locationid = 0
        else:
            cls.col = mongo_db["collLocationInfo"]
            doc_with_max_locationid = cls.col.find_one(sort=[("locationid", -1)])
            cls.locationid = doc_with_max_locationid['locationid'] if doc_with_max_locationid else 0


    def insert(cls, doc):
        try:
            if 'locationid' not in doc.keys():
                cls.locationid += 1
                doc['locationid'] = cls.locationid
            else:
                cls.locationid = doc['locationid']
            cls.col.insert_one(doc)
        except Exception:
            print("Error on insertion locationinfo occured")
        

    def delete(cls, locationid):
        print("on delete")
        print(locationid)
        cls.col.delete_one({'locationid': locationid})


    def update(cls, doc):
        doc = get_valid_fields(doc)
        cls.col.update_one({'locationid': doc['locationid']}, {'$set': doc})

    @classmethod
    def exists(cls, locationid):
        if mongo_db["collLocationInfo"].find_one({"locationid": locationid}):
            return True
        return False


    def info(cls):
        res = cls.col.find({}, {"_id": 0}, sort=[("locationid", -1)])
        result = [[el['areaname'], el['regname'], el['tername'], el['locationid']] for el in res]
        return result

class MongoInstitution:
    def __init__(cls):
        cls.validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["instid", "locationid", "instname"],
                "properties": {
                    "instname": {
                        "bsonType": "string"
                    },
                    "locationid": {
                        "bsonType": "int"
                    },
                    "insttype": {
                        "bsonType": ["string", "null"]
                    },
                    "instparent": {
                        "bsonType": ["string", "null"]
                    },
                    "instid": {
                        "bsonType": "int"
                    }
                }
            }
        }
        if "collInstitution" not in mongo_db.list_collection_names():  
            cls.col = mongo_db.create_collection('collInstitution', validator=cls.validator, validationAction="error")
            cls.instid = 0
        else:
            cls.col = mongo_db["collInstitution"]
            doc_with_max_instid = cls.col.find_one(sort=[("instid", -1)])
            cls.instid = doc_with_max_instid['instid'] if doc_with_max_instid else 0

    def insert(cls, doc):            
        try:
            if 'instid' not in doc.keys():
                cls.instid += 1
                doc['instid'] = cls.instid
            else:
                cls.instid = doc['instid']
            if 'locationid' not in doc.keys() or not MongoLocationInfo.exists(doc['locationid']):
                raise Exception("Location is not present in the database")
            cls.col.insert_one(doc)
        except Exception as ex:
            print(ex)
            print("Error on insertion institution occured")


    def delete(cls, instid):
        print("on delete:")
        print(instid)
        cls.col.delete_one({'instid': instid})
    

    def update(cls, doc):
        try:
            if 'locationid' in doc.keys() and not MongoLocationInfo.exists(doc['locationid']):
                raise Exception("Location is not present in the database")
            doc = get_valid_fields(doc)
            cls.col.update_one({'instid': doc['instid']}, {'$set': doc})
        except Exception as ex:
            print(ex)
            print("Couldn't update Institution")

    @classmethod
    def exists(cls, instid):
        if mongo_db["collInstitution"].find_one({"instid": instid}):
            return True
        return False

    def info(cls):
        res = cls.col.find({}, {"_id": 0},sort=[("instid", -1)])
        result = [[el['instname'], el['locationid'], el['insttype'], el['instparent'], el['instid']] for el in res]
        return result


class MongoStudent:
    def __init__(cls):
        cls.validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["outid", "locationid"],
                "properties": {
                    "outid": {
                        "bsonType": "string"
                    },
                    "birth": {
                        "bsonType": ["int", "null"]
                    },
                    "locationid": {
                        "bsonType": "int"
                    },
                    "sextypename": {
                        "bsonType": ["string", "null"]
                    },
                    "regtypename": {
                        "bsonType": ["string", "null"]
                    },
                    "classprofilename": {
                        "bsonType": ["string", "null"]
                    },
                    "classlangname": {
                        "bsonType": ["string", "null"]
                    },
                    "instid": {
                        "bsonType": ["int", "null"]
                    }
                }
            }
        }
        if "collStudent" not in mongo_db.list_collection_names():  
            cls.col = mongo_db.create_collection('collStudent', validator=cls.validator, validationAction="error")
        else:
            cls.col = mongo_db["collStudent"]


    def insert(cls, doc):            
        try:
            if 'outid' not in doc.keys():
                raise Exception("Outid is not provided")
            if 'locationid' not in doc.keys() or not MongoLocationInfo.exists(doc['locationid']):
                raise Exception("Location is not present in the database")
            if 'instid' not in doc.keys() or not MongoInstitution.exists(doc['instid']):
                raise Exception("Institution is not present in the database")          
            cls.col.insert_one(doc)
        except Exception as ex:
            print(ex)
            print("Error on insertion Student occured")


    def delete(cls, outid):
        cls.col.delete_one({'outid': outid})
    

    def update(cls, doc):
        try:
            if 'locationid' in doc.keys() and not MongoLocationInfo.exists(doc['locationid']):
                raise Exception("Location is not present in the database")
            if 'instid' in doc.keys() and not MongoInstitution.exists(doc['instid']):
                raise Exception("Institution is not present in the database")
            doc = get_valid_fields(doc)
            cls.col.update_one({'outid': doc['outid']}, {'$set': doc})
        except Exception as ex:
            print(ex)
            print("Couldn't update Student")

    @classmethod
    def exists(cls, outid):
        if mongo_db["collStudent"].find_one({"outid": outid}):
            return True
        return False

    def info(cls):
        res = cls.col.find({}, {"_id": 0})
        result = [[el['outid'], el['birth'], el['sextypename'], el['locationid'], el['regtypename'], el['classprofilename'], el['classlangname'], el['instid']] for el in res]
        return result


class MongoTest:
    def __init__(cls):
        cls.validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["testid", "instid", "outid"],
                "properties": {
                    "instid": {
                        "bsonType": "int"
                    },
                    "testyear": {
                        "bsonType": ["int", "null"]
                    },
                    "adaptscale": {
                        "bsonType": ["int", "null"]
                    },
                    "ball12": {
                        "bsonType": ["double", "null"]
                    },
                    "ball100": {
                        "bsonType": ["double", "null"]
                    },
                    "ball": {
                        "bsonType": ["double", "null"]
                    },
                    "subtest": {
                        "bsonType": ["bool", "null"]
                    },
                    "outid": {
                        "bsonType": "string"
                    },
                    "testname": {
                        "bsonType": "string"
                    },
                    "dpalevel": {
                        "bsonType": ["string", "null"]
                    },
                    "testlang": {
                        "bsonType": ["string", "null"]
                    },
                    "teststatus": {
                        "bsonType": "string"
                    },
                    "testid": {
                        "bsonType": "int"
                    }
                }
            }
        }
        if "collTest" not in mongo_db.list_collection_names():  
            cls.col = mongo_db.create_collection('collTest', validator=cls.validator, validationAction="error")
            cls.testid = 0
        else:
            cls.col = mongo_db["collTest"]
            doc_with_max_testid = cls.col.find_one(sort=[("testid", -1)])
            cls.testid = doc_with_max_testid['testid'] if doc_with_max_testid else 0

    def insert(cls, doc):            
        try:
            if 'testid' not in doc.keys():
                cls.testid += 1
                doc['testid'] = cls.testid
            else:
                cls.testid = doc['testid']
            if 'instid' not in doc.keys() or not MongoInstitution.exists(doc['instid']):
                raise Exception("Institution is not present in the database")
            if 'outid' not in doc.keys() or not MongoStudent.exists(doc['outid']):
                raise Exception("Student is not present in the database")
            cls.col.insert_one(doc)
        except Exception as ex:
            print(ex)
            print("Error on insertion test occured")


    def delete(cls, testid):
        cls.col.delete_one({'testid': testid})
    

    def update(cls, doc):
        try:                
            if 'instid' in doc.keys() and not MongoInstitution.exists(doc['instid']):
                raise Exception("Institution is not present in the database")
            if 'outid' in doc.keys() and not MongoStudent.exists(doc['outid']):
                raise Exception("Student is not present in the database")
            doc = get_valid_fields(doc)
            cls.col.update_one({'testid': doc['testid']}, {'$set': doc})
        except Exception as ex:
            print(ex)
            print("Couldn't update Test")

    @classmethod
    def exists(cls, testid):
        if mongo_db["collTest"].find_one({"testid": testid}):
            return True
        return False

    def info(cls):
        res = cls.col.find({}, {"_id": 0}, sort=[("testid", -1)])
        result = [[ el["instid"],
                    el["testyear"],
                    el["adaptscale"],
                    el["ball12"], 
                    el["ball100"],
                    el["ball"], 
                    el["subtest"], 
                    el["outid"],
                    el["testname"],
                    el["dpalevel"],
                    el["testlang"],
                    el["teststatus"],
                    el["testid"]] for el in res]
        return result

# needs realization
def get_statistics(years, regions, subjects, ball_function, teststatus):
    # get test ball 
    ball_function = "$" + ball_function
    query = mongo_db["collStudent"].aggregate([{
        "$lookup": {
            "from": "collLocationInfo", 
            "localField": "locationid", 
            "foreignField": "locationid", 
            "as": "location"
            }
        }, 
        {"$lookup": {
            "from": "collTest",
            "localField": "outid",
            "foreignField": "outid",
            "as": "test"
        }},
        {
            "$project": {
                "regname": "$location.regname",
                "testname": "$test.testname",
                "testyear": "$test.testyear",
                "ball100": "$test.ball100",
                "teststatus": "$test.teststatus"
            }
        }, 
        {"$unwind": "$regname"},
        {"$unwind": "$testname"},
        {"$unwind": "$testyear"},
        {"$unwind": "$ball100"},
        {"$unwind": "$teststatus"},
        { "$match": {
            "testname": {"$in": subjects},
            "regname": {"$in": regions},
            "testyear": {"$in": years},
            "teststatus": teststatus
            }
        },
        { "$group" : {
            "_id": {
                "testyear": "$testyear", 
                "regname": "$regname"
            },
            "ball": {
                ball_function: "$ball100"
            }
        }}])
    
    result = []
    for row in query:
        x = list(row.values())
        print(x)
        result.insert(list(x[0].values()) + x[-1])
    return result
    

def run_migrations():
    mongo_db["collLocationInfo"].drop()
    mongo_db["collInstitution"].drop()
    mongo_db["collStudent"].drop()
    mongo_db["collTest"].drop()
    migrate(query_locationinfo, "collLocationInfo")
    migrate(query_institution, "collInstitution")
    migrate(query_student, "collStudent")
    migrate(query_test, "collTest")
 
"""
a.
db.a.aggregate([{$match: {"testname": "ukr"}}, {$group: {_id: {testyear: "$testyear", areaname: "$student.location.areaname"}, 'avgball': {$avg: "$testball"} }}])

in testyear:
 db.a.aggregate([{$match: {"testname": "ukr", "testyear": {$in: [2003, 2009]}}}, {$group: {_id: {testyear: "$testyear", areaname: "$student.location.areaname"}, 'avgball': {$avg: "$testball"} }}])

 added area:
 db.a.aggregate([{$match: {"testname": "ukr", "testyear": {$in: [2003, 2009]}, "student.location.areaname": {$in: ['odeska', 'poltavska']}}}, {$group: {_id: 
{testyear: "$testyear", areaname: "$student.location.areaname"}, 'avgball': {$avg: "$testball"} }}])


"""