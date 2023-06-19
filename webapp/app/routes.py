from flask import redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,  SelectField, SelectMultipleField
from . import app, locations, institutions, students, tests, get_statistics
# from .models import get_statistics, get_locationinfo, insert_data, get_institution, get_student, get_test, delete_location, \
#     delete_institution, delete_student, delete_test, insert_institution, insert_student, insert_test, update_location, update_institution, \
#     update_student, update_test, insert_location, LocationInfo, Institution, Student, Test
from .models import PGLocationInfo, PGInstitution, PGStudent, PGTest, insert_data

# from sqlalchemy import MetaData, Table, insert, select, update, func, delete, desc, ForeignKey
# from .mongoModels import MongoLocationInfo, MongoInstitution, MongoStudent, MongoTest
# from .mongo_logics import *
# from . import engine


################################################
########### Migration to MongoDB ###############
################################################
# with engine.connect() as conn:
#     query_locations = select(LocationInfo).order_by(desc(LocationInfo.c.locationid))
#     locations = conn.execute(query_locations).all()
#     #print(locations[10][0], locations[10][1], locations[10][2], locations[10][3])
#     for loc in locations:
#         MongoLocationInfo.insert_data(loc[3], loc[2], loc[1], loc[0])
# print('Finish for LocationInfo')


# with engine.connect() as conn:
#     query_institution = select(Institution).order_by(desc(Institution.c.instid))
#     institutions = conn.execute(query_institution).all()
#     print(institutions[10][0], institutions[10][1], institutions[10][2], institutions[10][3], institutions[10][4])
#     for inst in institutions:
#         MongoInstitution.insert_data(inst[0], inst[1], inst[2], inst[3], inst[4])
# print('Finish for Institution')


# with engine.connect() as conn:
#     query_student = select(Student)
#     students = conn.execute(query_student).all()
#     print(students[100][0], students[100][1], students[100][2], students[100][3], students[100][4], students[100][5], students[100][6], students[100][7])
#     for stud in students:
#         MongoStudent.insert_data(stud[0], stud[1], stud[2], stud[3], stud[4], stud[5], stud[6], stud[7])
# print('Finish for Student')


# with engine.connect() as conn:
#     query_test = select(Test).order_by(desc(Test.c.testid))
#     tests = conn.execute(query_test).all()
#     print(tests[10][0], tests[10][1], tests[10][2], tests[10][3], tests[10][4], tests[10][5], tests[10][6], tests[10][7], tests[10][8], tests[10][9], tests[10][10], tests[10][11], tests[10][12])
#     for test in tests:
#         MongoTest.insert_data(test[0], test[1], test[2], test[3], test[4], test[5], test[6], test[7],
#                                  test[8], test[9], test[10], test[11], test[12])
# print('Finish for Test')

# print('Migrations for MongoDB were finished')
###########################################

# n = int(input('for mongo input 1: '))
# n = 2
# if n == 1:
#     db = 'mongo'
#     locations = MongoLocationInfo()
#     institutions = MongoInstitution()
#     students = MongoStudent()
#     tests = MongoTest()
# else:
#     db = 'postgres'
#     locations = PGLocationInfo()
#     institutions = PGInstitution()
#     students = PGStudent()
#     tests = PGTest()


sub =[('Українська мова і література', 'Українська мова і література'),  ('Англійська мова', 'Англійська мова'),
      ('Французька мова', 'Французька мова'), ('Іспанська мова', 'Іспанська мова'), ('Німецька мова', 'Німецька мова'),
      ('Математика', 'Математика'), ('Математика (завдання рівня стандарту)', 'Математика (завдання рівня стандарту)'),
      ('Географія', 'Географія'), ('Біологія', 'Біологія'), ('Російська мова', 'Російська мова'),
      ('Історія України', 'Історія України'), ('Фізика', 'Фізика'), ('Хімія', 'Хімія'), ('Українська мова', 'Українська мова')]

reg = [("all", "Всі"), ("Вінницька область", "Вінницька область"), ("Волинська область", "Волинська область"),
       ("Дніпропетровська область", "Дніпропетровська область"), ("Донецька область", "Донецька область"),
       ("Житомирська область", "Житомирська область"), ("Закарпатська область", "Закарпатська область"),
       ("Запорізька область", "Запорізька область"), ("Івано-Франківська область", "Івано-Франківська область"),
       ("Київська область", "Київська область"), ("Кіровоградська область", "Кіровоградська область"),
       ("Луганська область", "Луганська область"), ("Львівська область", "Львівська область"),
       ("Миколаївська область", "Миколаївська область"), ("м.Київ", "м.Київ"),
       ("Одеська область", "Одеська область"), ("Полтавська область", "Полтавська область"),
       ("Рівненська область", "Рівненська область"), ("Сумська область", "Сумська область"),
       ("Тернопільська область", "Тернопільська область"), ("Харківська область", "Харківська область"),
       ("Херсонська область", "Херсонська область"), ("Хмельницька область", "Хмельницька область"),
       ("Черкаська область", "Черкаська область"), ("Чернівецька область", "Чернівецька область"),
       ("Чернігівська область", "Чернігівська область")]

reg_all = ["Вінницька область", "Волинська область", "Дніпропетровська область", "Донецька область",
           "Житомирська область", "Закарпатська область", "Запорізька область", "Івано-Франківська область",
           "Київська область", "Кіровоградська область", "Луганська область", "Львівська область",
           "Миколаївська область", "м.Київ", "Одеська область", "Полтавська область", "Рівненська область",
           "Сумська область", "Тернопільська область", "Харківська область", "Херсонська область",
           "Хмельницька область", "Черкаська область", "Чернівецька область", "Чернігівська область"]

test_year = [(2016, '2016'), (2017, '2017'), (2018, '2018'), (2019, '2019'), (2020, '2020'), (2021, '2021')]
ball_func = [('min', 'Min'), ('max', 'Max'), ('avg', 'Avg')]

class Statistic(FlaskForm):
    subject = SelectField('subject', choices=sub, coerce=str)
    year = SelectMultipleField('year', choices=test_year, coerce=int)
    region = SelectMultipleField('region', choices=reg, coerce=str)
    ball_function = SelectField('ball_function', choices=ball_func, coerce=str)
    submit = SubmitField("Submit")

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except Exception:
        return default

@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')


@app.route('/location_info', methods=['GET', 'POST'])
def location_info():
    columns = ("AreaName", "RegName", "TerName", "LocationID", "Delete Button")
    result = locations.info()[:1000]
    # locations = MongoLocationInfo.info()[:1000]
    # print(f'Database: {db}')
    # print(locations[10])
    return render_template('location.html', columns=columns, locations=result)


@app.route('/location_info/insert_locationinfo', methods=['POST'])
def insert_locationinfo():
    new_row = {'areaname': request.form['areaname'],
               'tername': request.form['tername'],
               'regname': request.form['regname']}
    if all([value is not None for value in new_row.values()]):
        locations.insert(new_row)
        # insert_location(new_row)
    return redirect(url_for('location_info'))

    
@app.route('/location_info/update_locationinfo', methods=['POST'])
def update_locationinfo():
    values_on_update = {'locationid': safe_cast(request.form['locationid'], int),
                        'areaname': request.form['areaname'],
                        'tername': request.form['tername'],
                        'regname': request.form['regname']}
    if values_on_update['locationid']:
        locations.update(values_on_update)
        # update_location(values_on_update)        
    return redirect(url_for('location_info'))
    

@app.route('/location_info/del_location', methods=['POST'])
def del_location():
    location_id = safe_cast(request.form['locationid'], int)
    locations.delete(location_id)
    # delete_location(location_id)
    return redirect(url_for('location_info'))


@app.route('/institution_info', methods=['GET', 'POST'])
def institution_info():
    columns = ("InstitutionName", "LocationID", "InstitutionType", "Parent", "InstitutionID", "Delete Button")
    result = institutions.info()[:1000]
    # institutions = get_institution()[:1000]
    return render_template('institution.html', columns=columns, institutions=result)


@app.route('/institution_info/insert_inst', methods=['POST'])
def insert_inst():
    row_to_insert = {'instname': request.form['instname'],
                    'locationid': safe_cast(request.form['locationid'], int),
                    'insttype': request.form['insttype'],
                    'instparent': request.form['instparent']}
    if all([value is not None for value in [row_to_insert['instname'], row_to_insert['locationid']]]):
        # insert_institution(row_to_insert)
        institutions.insert(row_to_insert)
    return redirect(url_for('institution_info'))


@app.route('/institution_info/update_institutioninfo', methods=['POST'])
def update_institutioninfo():
    values_on_update = {'instid': safe_cast(request.form['instid'], int),
                        'instname': request.form['instname'],
                        'locationid': safe_cast(request.form['locationid'], int),
                        'insttype': request.form['insttype'],
                        'instparent': request.form['instparent']}
    if values_on_update['instid']:
        institutions.update(values_on_update)
        # update_institution(values_on_update)        
    return redirect(url_for('institution_info'))


@app.route('/institution_info/del_institution', methods=['POST'])
def del_institution():
    inst_Id = safe_cast(request.form['instid'], int)
    institutions.delete(inst_Id)
    # delete_institution(inst_Id)
    return redirect(url_for('institution_info'))


@app.route('/student_info/insert_studentinfo', methods=['POST'])
def insert_studentinfo():
    row_to_insert =     {'outid': request.form['outid'],
                        'birth': safe_cast(request.form['birth'], int),
                        'locationid': safe_cast(request.form['locationid'], int),
                        'sextypename': request.form['sextypename'],
                        'regtypename': request.form['regtypename'],
                        'classprofilename': request.form['classprofilename'],
                        'classlangname': request.form['classlangname'],
                        'instid': safe_cast(request.form['instid'], int)}
    if all([value is not None for value in [row_to_insert['outid'], row_to_insert['locationid']]]):
        students.insert(row_to_insert)
        # insert_student(row_to_insert)
    return redirect(url_for('student_info'))


@app.route('/student_info/update_studentinfo', methods=['POST'])
def update_studentinfo():
    values_on_update = {'outid': request.form['outid'],
                        'birth': safe_cast(request.form['birth'], int),
                        'locationid': safe_cast(request.form['locationid'], int),
                        'sextypename': request.form['sextypename'],
                        'regtypename': request.form['regtypename'],
                        'classprofilename': request.form['classprofilename'],
                        'classlangname': request.form['classlangname'],
                        'instid': safe_cast(request.form['instid'], int)}
    if values_on_update['outid']:
        students.update(values_on_update)
        # update_student(values_on_update)        
    return redirect(url_for('student_info'))


@app.route('/student_info', methods=['GET', 'POST'])
def student_info():
    columns = ("OUTID", "Birth", "SexType", "LocationID", "StudentType", "ProfileName", "ClassLang", "InstitutionID", "Delete Button")
    result = students.info()[:1000]
    # students = get_student()[:1000]
    return render_template('student.html', columns=columns, students=result)


@app.route('/student_info/del_student', methods=['POST'])
def del_student():
    outid = request.form['outid']
    students.delete(outid)
    # delete_student(outid)
    return redirect(url_for('student_info'))


@app.route('/test_info/insert_testinfo', methods=['POST'])
def insert_testinfo():
    row_to_insert =     {'instid': safe_cast(request.form['instid'], int),
                        'testyear': safe_cast(request.form['testyear'], int),
                        'adaptscale': safe_cast(request.form['adaptscale'], int),
                        'ball12': safe_cast(request.form['ball12'], float),
                        'ball100': safe_cast(request.form['ball100'], float),
                        'ball': safe_cast(request.form['ball'], float),
                        'subtest': safe_cast(request.form['subtest'], lambda x: True if x.lower() == 'так' else False),
                        'outid': request.form['outid'],
                        'testname': request.form['testname'],
                        'dpalevel': request.form['dpalevel'],
                        'testlang': request.form['testlang'],
                        'teststatus': request.form['teststatus']}
    if all([value is not None for value in [row_to_insert['instid'], row_to_insert['testyear'], row_to_insert['outid'], row_to_insert['testname']]]):
        tests.insert(row_to_insert)
        # insert_test(row_to_insert)
    return redirect(url_for('test_info'))


@app.route('/test_info', methods=['GET', 'POST'])
def test_info():
    columns = ("InstitutionID", "TestYear", "AdaptScale", "Ball12", "Ball100", "Ball", "SubTest", "OUTID", "Subject", "DPALevel",
               "Lang", "TestStatus", "TestID", "Delete Button")
    result = tests.info()[:1000]
    # tests = get_test()[:1000]
    return render_template('test.html', columns=columns, tests=result)


@app.route('/test_info/del_test', methods=['POST'])
def del_test():
    testId = safe_cast(request.form['testid'], int)
    tests.delete(testId)
    # delete_test(testId)
    return redirect(url_for('test_info'))

@app.route('/test_info/update_testinfo', methods=['POST'])
def update_testinfo():
    values_on_update = {'testid': safe_cast(request.form['testid'], int),
                        'instid': safe_cast(request.form['instid'], int),
                        'testyear': safe_cast(request.form['testyear'], int),
                        'adaptscale': safe_cast(request.form['adaptscale'], int),
                        'ball12': safe_cast(request.form['ball12'], float),
                        'ball100': safe_cast(request.form['ball100'], float),
                        'ball': safe_cast(request.form['ball'], float),
                        'subtest': safe_cast(request.form['subtest'], lambda x: True if x.lower() == 'так' else False),
                        'outid': request.form['outid'],
                        'testname': request.form['testname'],
                        'dpalevel': request.form['dpalevel'],
                        'testlang': request.form['testlang'],
                        'teststatus': request.form['teststatus']}
    if values_on_update['testid']:
        tests.update(values_on_update)
        # update_test(values_on_update)        
    return redirect(url_for('test_info'))


# створити роут для вставки в базу
@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
    # write here maps of forms
        values = {
        'student_id': request.form["student_id"],
        'student_birth': safe_cast(request.form["student_birth"], int),
        'student_sex': request.form["student_sex"],
        'student_area': request.form["student_area"],
        'student_region': request.form["student_region"],
        'student_ter': request.form["student_ter"],
        'student_regtype': request.form["student_regtype"],
        'class_profile': request.form["class_profile"],
        'class_lang': request.form["class_lang"],
        'student_inst_name': request.form["student_inst_name"],
        'student_inst_area': request.form["student_inst_area"],
        'student_inst_region': request.form["student_inst_region"],
        'student_inst_ter': request.form["student_inst_ter"],
        'student_inst_type': request.form["student_inst_type"],
        'student_inst_parent': request.form["student_inst_parent"],
        'test_name': request.form["test_name"],
        'test_inst_name': request.form["test_inst_name"],
        'test_inst_area': request.form["test_inst_area"],
        'test_inst_region': request.form["test_inst_region"],
        'test_inst_ter': request.form["test_inst_ter"],
        'test_year': safe_cast(request.form["test_year"], int),
        'adapt_scale': safe_cast(request.form["adapt_scale"], int),
        'ball12': safe_cast(request.form["ball12"], float),
        'ball100': safe_cast(request.form["ball100"], float),
        'ball': safe_cast(request.form["ball"], float),
        'subtest': safe_cast(request.form["subtest"], lambda x: True if x.lower() == 'так' else False),
        'dpalevel': request.form["dpalevel"],
        'test_lang': request.form["test_lang"],
        'test_status': request.form["test_status"]}

        insert_data(values)
        return redirect(url_for('main_page'))
    return render_template('addNew.html')


@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    headers = ("Рік", "Регіон", "Бал")
    result = []
    # query parameters
    form = Statistic(request.form)
    if request.method == 'POST':
        subject = request.form.get("subject")
        years = request.form.getlist("year")
        regions = request.form.getlist("region")
        ball_function = request.form.get("ball_function")

        print(subject)
        print(years)
        print(regions)
        print(ball_function)
        if 'all' in regions:
            regions = reg_all
        years = [safe_cast(year, int) for year in years]
        result = get_statistics(years=years, regions=regions, subject=subject, ball_function=ball_function, teststatus='Зараховано')
    return render_template('statistics.html', form=form, headers=headers, statistics_data=result)
