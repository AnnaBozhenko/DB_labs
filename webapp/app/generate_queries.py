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

def create_index_on_locationinfo():
    q = "create index if not exists locInfo on locationInfo(areaName, regName, terName);\n\n"
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
    LocationInfo.terName = examinations.{test}pttername)""" for test in TESTS]) + ";\n"
    q += """
alter table Institution add column instId serial primary key;
alter table Institution add constraint fk_location foreign key (locationId) references LocationInfo (locationId) on delete cascade;\n"""
    return q

def q_create_student_1():
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
    LocationInfo.tername = examinations.tername);

alter table Student add column instId integer;"""
    return q

def q_create_student_2():
    q = """
create table if not exists temp as
select 
    instId,
    instName,
    areaName,
    regName,
    terName
from Institution 
inner join LocationInfo on
    Institution.locationId = LocationInfo.locationId;
    
create index if not exists temp_inst on temp(instName, areaName, regName, terName);"""
    return q

def q_create_student_3():
    q = """
update Student
    set instId = temp.instId
from temp
where temp.instName = Student.eoname and
      temp.areaName = Student.eoareaname and
      temp.regName = Student.eoregname and
      temp.terName = Student.eotername;"""
    return q
    
def q_create_student_4():
    q = """
drop table temp;
alter table Student drop column eoname;
alter table Student drop column eoareaname;
alter table Student drop column eoregname;
alter table Student drop column eotername;

alter table Student add constraint pk_student primary key (outId);
alter table Student add constraint fk_location foreign key (locationId) references LocationInfo (locationId) on delete cascade;
alter table Student add constraint fk_institution foreign key (instId) references Institution (instId) on delete cascade;\n"""
    return q

def q_create_test_1():
    q = """
create table if not exists test 
   (instId     integer,
    testYear   smallint,
    adaptScale smallint,
    ball12     numeric(4, 1),
    ball100    numeric(4, 1),
    ball       numeric(4, 1),
    subtest    boolean,
    outid      varchar,
    testName   varchar,
    dpaLevel   varchar,
    testLang   varchar,
    testStatus varchar);

-- populate with ukr-test
insert into test 
    (instId,    
    testYear,  
    adaptScale,
    ball12,    
    ball100,   
    ball,      
    subtest,   
    outid,     
    testName,  
    testStatus) 
select
    instId,    
    testYear,  
    ukradaptScale,
    ukrball12,    
    ukrball100,   
    ukrball,      
    ukrsubtest,   
    outid,     
    ukrtest,  
    ukrtestStatus
from examinations 
inner join locationInfo ON
    ukrptareaname = locationInfo.areaName AND
    ukrptregname = locationInfo.regName AND
    ukrpttername = locationInfo.terName
inner join institution on 
    institution.instname = ukrptname AND
    institution.locationId = locationInfo.locationId;

-- populate with uml-test
insert into test
(instId,    
    testYear,  
    ball12,    
    ball100,   
    ball,      
    outid,     
    testName,  
    testStatus)
select
instId,    
    testYear,  
    umlball12,    
    umlball100,   
    umlball,      
    outid,     
    umltest,  
    umltestStatus
from examinations
inner join locationInfo ON
    umlptareaname = locationInfo.areaName AND
    umlptregname = locationInfo.regName AND
    umlpttername = locationInfo.terName
inner join institution on 
    institution.instname = umlptname AND
    institution.locationId = locationInfo.locationId;

-- populate with math-test
insert into test
(   instId,    
    testYear,  
    ball12,    
    ball100,   
    ball,      
    outid,     
    testName,  
    dpaLevel,  
    testLang,  
    testStatus)
select
    instId,    
    testYear,  
    mathball12,    
    mathball100,   
    mathball,      
    outid,     
    mathtest,  
    mathdpaLevel,  
    mathlang,  
    mathtestStatus
from examinations
inner join locationInfo ON
    mathptareaname = locationInfo.areaName AND
    mathptregname = locationInfo.regName AND
    mathpttername = locationInfo.terName
inner join institution on 
    institution.instname = mathptname AND
    institution.locationId = locationInfo.locationId;

-- populate with mathst-test
insert into test
    (instId,    
    testYear,  
    ball12,    
    ball,      
    outid,     
    testName,  
    testLang,  
    testStatus)
select
    instId,    
    testYear,  
    mathstball12,    
    mathstball,      
    outid,     
    mathsttest,  
    mathstlang,  
    mathsttestStatus
from examinations
inner join locationInfo ON
    mathstptareaname = locationInfo.areaName AND
    mathstptregname = locationInfo.regName AND
    mathstpttername = locationInfo.terName
inner join institution on 
    institution.instname = mathstptname AND
    institution.locationId = locationInfo.locationId;

-- populate with rus-test
insert into test
    (instId,    
    testYear,  
    ball12,    
    ball100,   
    outid,     
    testName,  
    testStatus)
select 
    instId,    
    testYear,  
    rusball12,    
    rusball100,   
    outid,     
    rustest,  
    rustestStatus 
from examinations
inner join locationInfo ON
    rusptareaname = locationInfo.areaName AND
    rusptregname = locationInfo.regName AND
    ruspttername = locationInfo.terName
inner join institution on 
    institution.instname = rusptname AND
    institution.locationId = locationInfo.locationId;
"""
    q += "".join([f"""
insert into test
    (instId,    
    testYear,  
    ball12,    
    ball100,   
    ball,      
    outid,     
    testName,
    testLang,  
    testStatus)
select 
    instId,    
    testYear,  
    {test}ball12,    
    {test}ball100,   
    {test}ball,      
    outid,     
    {test}test,
    {test}lang,  
    {test}testStatus
from examinations
inner join locationInfo ON
    {test}ptareaname = locationInfo.areaName AND
    {test}ptregname = locationInfo.regName AND
    {test}pttername = locationInfo.terName
inner join institution on 
    institution.instname = {test}ptname AND
    institution.locationId = locationInfo.locationId;
""" for test in ['geo', 'bio', 'hist', 'phys', 'chem']])
    q += "".join([f"""
insert into test
    (instId,    
    testYear,  
    ball12,    
    ball100,   
    ball,      
    outid,     
    testName,  
    dpaLevel,  
    testStatus)
select 
    instId,    
    testYear,  
    {test}ball12,    
    {test}ball100,   
    {test}ball,      
    outid,     
    {test}test,  
    {test}dpaLevel,  
    {test}testStatus
from examinations
inner join locationInfo ON
    {test}ptareaname = locationInfo.areaName AND
    {test}ptregname = locationInfo.regName AND
    {test}pttername = locationInfo.terName
inner join institution on 
    institution.instname = {test}ptname AND
    institution.locationId = locationInfo.locationId;
""" for test in ['eng', 'fr', 'sp', 'deu']])
    return q

def q_create_test_2():
    q = """
delete from Test where testname is null;
alter table Test add column testId serial;

alter table Test add constraint pk_test_student primary key (testId);
alter table Test add constraint fk_institution foreign key (instId) references Institution (instId) on delete cascade;
alter table Test add constraint fk_student foreign key (outId) references Student (outId) on delete cascade;\n\n"""
    return q

def q_clean_unnecessary_structures():
    q = """
drop index locInfo;
drop table examinations;
"""
    return q


        
