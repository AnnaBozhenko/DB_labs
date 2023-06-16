#from webapp.config import mongo_db
import pymongo

mongo_client = pymongo.MongoClient('mongodb://user:pass@mongodb:27017/')
mongo_db = mongo_client['zno']


class MongoLocationInfo:
    col = mongo_db['collLocationInfo']
    doc = {
        'locationid': 'NULL',
        'areaname': 'NULL',
        'regname': 'NULL',
        'tername': 'NULL'
    }

    @classmethod
    def insert_data(cls, locationid, areaname, regname, tername):
        if locationid == 'NoneType':
            return f''
        doc = {
            'locationId': int(locationid),
            'areaname': str(areaname) if areaname is not None else 'NULL',
            'regname': str(regname) if regname is not None else 'NULL',
            'tername': str(tername) if tername is not None else 'NULL'
        }
        return cls.col.insert_one(doc)

    @classmethod
    def delete_data(cls, locationid):
        del_query = {'locationId': locationid}
        return cls.col.delete_one(del_query)

    @classmethod
    def update_data(cls, locationid, areaname, tername, regname):
        cur_query = {'locationid': locationid}
        up_query = {'$set': {'areaname': areaname,
                             'tername': tername,
                             'regname': regname}
                    }
        return cls.col.update_one(cur_query, up_query)

    @classmethod
    def info(cls):
        res = cls.col.find({}, {"_id": 0})
        result = []
        for i in res:
            result.append(i.values())
        return result

class MongoInstitution:
    col = mongo_db['collInstitution']
    doc = {
        'instname': 'NULL',
        'locationid': 'NULL',
        'insttype': 'NULL',
        'instparent': 'NULL',
        'instid': 'NULL'
    }

    @classmethod
    def insert_data(cls, instname, locationid, insttype, instparent, instid):
        if instid == 'NoneType':
            return f''
        doc = {
            'instname': str(instname) if instname is not None else 'NULL',
            'locationid': int(locationid),
            'insttype': str(insttype) if insttype is not None else 'NULL',
            'instparent': str(instparent) if instparent is not None else 'NULL',
            'instid': int(instid)
        }
        return cls.col.insert_one(doc)

    # @classmethod
    # def delete_data(cls, locationid):
    #     del_query = {'locationId': locationid}
    #     return cls.col.delete_one(del_query)
    #
    # @classmethod
    # def update_data(cls, locationid, areaname, tername, regname):
    #     cur_query = {'locationid': locationid}
    #     up_query = {'$set': {'areaname': areaname,
    #                          'tername': tername,
    #                          'regname': regname}
    #                 }
    #     return cls.col.update_one(cur_query, up_query)

    @classmethod
    def info(cls):
        res = cls.col.find({}, {"_id": 0})
        result = []
        for i in res:
            result.append(i.values())
        return result


class MongoStudent:
    col = mongo_db['collStudent']
    doc = {
        'outid': 'NULL',
        'birth': 'NULL',
        'sextypename': 'NULL',
        'locationid': 'NULL',
        'regtypename': 'NULL',
        'classprofilename': 'NULL',
        'classlangname': 'NULL',
        'instid': 'NULL'
    }

    @classmethod
    def insert_data(cls, outid, birth, sextypename, locationid, regtypename, classprofilename, classlangname, instid):
        if outid == 'NoneType':
            return f''
        doc = {
            'outid': str(outid),
            'birth': int(birth),
            'sextypename': str(sextypename) if sextypename is not None else 'NULL',
            'locationid': int(locationid),
            'regtypename': str(regtypename) if regtypename is not None else 'NULL',
            'classprofilename': str(classprofilename) if classprofilename is not None else 'NULL',
            'classlangname': str(classlangname) if classlangname is not None else 'NULL',
            'instid': int(instid) if instid is not None else 'NULL'
        }
        return cls.col.insert_one(doc)

    # @classmethod
    # def delete_data(cls, locationid):
    #     del_query = {'locationId': locationid}
    #     return cls.col.delete_one(del_query)
    #
    # @classmethod
    # def update_data(cls, locationid, areaname, tername, regname):
    #     cur_query = {'locationid': locationid}
    #     up_query = {'$set': {'areaname': areaname,
    #                          'tername': tername,
    #                          'regname': regname}
    #                 }
    #     return cls.col.update_one(cur_query, up_query)

    @classmethod
    def info(cls):
        res = cls.col.find({}, {"_id": 0})
        result = []
        for i in res:
            result.append(i.values())
        return result


class MongoTest:
    col = mongo_db['collTest']
    doc = {
        'instid': 'NULL',
        'testyear': 'NULL',
        'adaptscale': 'NULL',
        'ball12': 'NULL',
        'ball100': 'NULL',
        'ball': 'NULL',
        'subtest': 'NULL',
        'outid': 'NULL',
        'testname': 'NULL',
        'dpalevel': 'NULL',
        'testlang': 'NULL',
        'teststatus': 'NULL',
        'testid': 'NULL'
    }

    @classmethod
    def insert_data(cls, instid, testyear, adaptscale, ball12, ball100, ball, subtest, outid, testname, dpalevel,
                    testlang, teststatus, testid):
        if testid == 'NoneType':
            return f''
        doc = {
            'instid': int(instid),
            'testyear': int(testyear),
            'adaptscale': int(adaptscale),
            'ball12': float(ball12),
            'ball100': float(ball100),
            'ball': float(ball),
            'subtest': str(subtest) if subtest is not None else 'NULL',
            'outid': str(outid),
            'testname': str(testname),
            'dpalevel': str(dpalevel) if dpalevel is not None else 'NULL',
            'testlang': str(testlang) if testlang is not None else 'NULL',
            'teststatus': str(teststatus) if teststatus is not None else 'NULL',
            'testid': int(testid)
        }
        return cls.col.insert_one(doc)

    # @classmethod
    # def delete_data(cls, locationid):
    #     del_query = {'locationId': locationid}
    #     return cls.col.delete_one(del_query)
    #
    # @classmethod
    # def update_data(cls, locationid, areaname, tername, regname):
    #     cur_query = {'locationid': locationid}
    #     up_query = {'$set': {'areaname': areaname,
    #                          'tername': tername,
    #                          'regname': regname}
    #                 }
    #     return cls.col.update_one(cur_query, up_query)

    @classmethod
    def info(cls):
        res = cls.col.find({}, {"_id": 0})
        result = []
        for i in res:
            result.append(i.values())
        return result