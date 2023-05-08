TESTS = ['ukr', 'uml', 'eng', 'fr', 'sp', 'deu', 'math', 'mathst', 'geo', 'bio', 'rus', 'hist', 'phys', 'chem']

def q_create_locationInfo():
    areas =       [test + 'ptareaname' for test in TESTS] + ['areaname', 'eoareaname']
    regions =     [test + 'ptregname' for test in TESTS] + ['regname', 'eoregname']
    territories = [test + 'pttername' for test in TESTS] + ['tername','eotername']
    q = "create table if not exists LocationInfo as ("
    q += '\n union \n'.join([f"""select
    {a} as areaName,
    {r} as regName,
    {t} as terName 
from examinations""" for a, r, t in zip(areas, regions, territories)]) + ");\n\n"
    q += "alter table LocationInfo add column locationId serial primary key;\n"
    return q
    
def q_create_institution():
    q = """create table if not exists Institution as 
(select 
    eoname as instName,
    locationId,
    eotypename as instType,
    eoparent as instParent
from examinations 
inner join LocationInfo on
    LocationInfo.areaname = examinations.eoareaname and
    LocationInfo.regname = examinations.eoregname and
    LocationInfo.tername = examinations.eotername) \n union \n"""
    q += "\n union \n".join([f"""(select
    {test}ptname as instName,
    locationId,
    NULL as instType,
    NULL as instParent
from examinations 
inner join LocationInfo on 
    LocationInfo.areaName = examinations.{test}ptareaname and
    LocationInfo.regName = examinations.{test}ptregname and
    LocationInfo.terName = examinations.{test}pttername)""" for test in TESTS]) + ";\n\n"
    q += "alter table Institution add column instId serial primary key;\n\n"
    q += "alter table Institution add constraint fk_location foreign key (locationId) references LocationInfo (locationId);\n\n"
    return q


def q_create_student():
    q = """create table if not exists Student as
(select 
    outId,
    birth,
    sexTypeName,
    locationId,
    regTypeName,
    classProfileName,
    classLangName,
    eoname,
    eoareaname,
    eoregname,
    eotername
from examinations
inner join LocationInfo on
    LocationInfo.areaname = examinations.areaname and
    LocationInfo.regname = examinations.regname and
    LocationInfo.tername = examinations.tername);\n\n"""
    q += "alter table Student add column instId integer;\n\n"
    q += """update Student
    set instId = temp.instId
from
(select 
    instId,
    instName,
    areaName,
    regName,
    terName
from Institution 
inner join LocationInfo on
    Institution.locationId = LocationInfo.locationId) temp
where temp.instName = Student.eoname and
      temp.areaName = Student.eoareaname and
      temp.regName = Student.eoregname and
      temp.terName = Student.eotername;\n"""
    q += """
alter table Student drop column eoname;
alter table Student drop column eoareaname;
alter table Student drop column eoregname;
alter table Student drop column eotername;

alter table Student add constraint pk_student primary key (outId);
alter table Student add constraint fk_location foreign key (locationId) references LocationInfo (locationId);
alter table Student add constraint fk_institution foreign key (instId) references Institution (instId);\n"""
    return q


# create tables for each test seperatly and then unite them into one table
def q_create_test():
    q = """create table if not exists Test as
(select 
    outId,
    testYear,
    ukradaptscale as adaptScale,
    ukrsubtest as subtest,
    ukrtest as testName,
    ukrball12 as ball12,
    ukrball100 as ball100,
    ukrball as ball,
    NULL as dpalevel,
    NULL as testLang,
    ukrteststatus as testStatus,
    ukrptname as instName,
    ukrptareaname as instAreaName,
    ukrptregname as instRegName,
    ukrpttername as instTerName
from examinations)\n union \n"""
    q += """(select 
    outId,
    testYear,
    NULL as adaptScale,
    NULL as subtest,
    umltest as testName,
    umlball12 as ball12,
    umlball100 as ball100,
    umlball as ball,
    NULL as dpalevel,
    NULL as testLang,
    umlteststatus as testStatus,
    umlptname as instName,
    umlptareaname as instAreaName,
    umlptregname as instRegName,
    umlpttername as instTerName
from examinations)\n union \n"""
    q += "\n union \n".join([f"""(select 
    outId,
    testYear,
    NULL as adaptScale,
    NULL as subtest,
    {test}test as testName,
    {test}ball12 as ball12,
    {test}ball100 as ball100,
    {test}ball as ball,
    NULL as dpalevel,
    {test}lang as testLang,
    {test}teststatus as testStatus,
    {test}ptname as instName,
    {test}ptareaname as instAreaName,
    {test}ptregname as instRegName,
    {test}pttername as instTerName
from examinations)""" for test in ['geo', 'bio', 'hist', 'phys', 'chem']])
    q += "\n union \n" + "\n union \n".join([f"""(select 
    outId,
    testYear,
    NULL as adaptScale,
    NULL as subtest,
    {test}test as testName,
    {test}ball12 as ball12,
    {test}ball100 as ball100,
    {test}ball as ball,
    {test}dpalevel as dpalevel,
    NULL as testLang,
    {test}teststatus as testStatus,
    {test}ptname as instName,
    {test}ptareaname as instAreaName,
    {test}ptregname as instRegName,
    {test}pttername as instTerName
from examinations)""" for test in ['eng', 'fr', 'sp', 'deu']])
    q += """
 union
(select 
    outId,
    testYear,
    NULL as adaptScale,
    NULL as subtest,
    mathtest as testName,
    mathball12 as ball12,
    mathball100 as ball100,
    mathball as ball,
    mathdpalevel as dpalevel,
    mathlang as testLang,
    mathteststatus as testStatus,
    mathptname as instName,
    mathptareaname as instAreaName,
    mathptregname as instRegName,
    mathpttername as instTerName
from examinations)
 union
(select 
    outId,
    testYear,
    NULL as adaptScale,
    NULL as subtest,
    mathsttest as testName,
    mathstball12 as ball12,
    NULL as ball100,
    mathstball as ball,
    NULL as dpalevel,
    mathstlang as testLang,
    mathstteststatus as testStatus,
    mathstptname as instName,
    mathstptareaname as instAreaName,
    mathstptregname as instRegName,
    mathstpttername as instTerName
from examinations)
 union
(select 
    outId,
    testYear,
    NULL as adaptScale,
    NULL as subtest,
    rustest as testName,
    rusball12 as ball12,
    rusball100 as ball100,
    NULL as ball,
    NULL as dpalevel,
    NULL as testLang,
    rusteststatus as testStatus,
    rusptname as instName,
    rusptareaname as instAreaName,
    rusptregname as instRegName,
    ruspttername as instTerName
from examinations);\n\n"""
    q += "alter table Test add column testId serial;\n\n"
    q += "alter table Test add column instId integer;\n\n"
    q += """update Test
    set instId = temp.instId
from (select 
    instId,
    instName,
    areaName,
    regName,
    terName
from Institution
inner join LocationInfo on
    Institution.locationId = LocationInfo.locationId) temp
where Test.instName = temp.instName and
    Test.instAreaName = temp.areaName and
    Test.instRegName = temp.regName and
    Test.instTerName = temp.terName;\n"""
    q += """
alter table Test drop column instName;
alter table Test drop column instAreaName;
alter table Test drop column instRegName;
alter table Test drop column instTerName;

delete from Test where testname is null;

alter table Test add constraint pk_test_student primary key (outId, testId);
-- alter table Test add constraint fk_institution foreign key (instId) references Institution (instId);
-- alter table Test add constraint fk_student foreign key (outId) references Student (outId);\n\n"""
    return q
