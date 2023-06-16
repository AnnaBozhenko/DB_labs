import pymongo

mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['zno']

class MongoLocationInfo:
    col = mongo_db('collLocationInfo')
    doc = {
        'locationid': 'NULL',
        'areaname': 'NULL',
        'regname': 'NULL',
        'tername': 'NULL'
    }

    @classmethod
    def insert_data(cls, locationid, areaname, regname, tername):
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
        res = list(cls.col.find({}))
        return res

