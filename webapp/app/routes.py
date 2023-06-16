from flask import redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,  SelectField, SelectMultipleField
from . import app
from .models import get_statistics, get_locationinfo, insert_data, get_institution, get_student, get_test, delete_location, \
    delete_institution, delete_student, delete_test, insert_institution, insert_student, insert_test, update_location, update_institution, \
    update_student, update_test, insert_location, LocationInfo

from sqlalchemy import MetaData, Table, insert, select, update, func, delete, desc, ForeignKey
from .mongoModels import MongoLocationInfo
from . import engine


################################################
########### Migration to MongoDB ###############
################################################
with engine.connect() as conn:
    query_locations = select(LocationInfo).order_by(desc(LocationInfo.c.locationid))
    locations = conn.execute(query_locations).all()
    i = 0
    for loc in locations:
        if i % 1000 == 0:
            print(loc[3], loc[2], loc[1], loc[0])
        MongoLocationInfo.insert_data(loc[3], loc[2], loc[1], loc[0])
        i += 1
print('Finish for LocationInfo')
###########################################

# n = int(input('for mongo input 1: '))
n = 1
if n == 1:
    db = 'mongo'
else:
    db = 'postgres'

class UpdateTables(FlaskForm):
    student_id = StringField('student_id')
    student_birth = IntegerField('student_birth')
    student_sex = StringField('student_sex')
    student_area = StringField('student_area')
    student_region = StringField('student_region')
    student_ter = StringField('student_ter')
    student_regtype = StringField('student_regtype')
    class_profile = StringField('class_profile')
    class_lang = StringField('class_lang')
    student_inst_name = StringField('student_inst_name')
    student_inst_area = StringField('student_inst_area')
    student_inst_region = StringField('student_inst_region')
    student_inst_ter = StringField('student_inst_ter')
    student_inst_type = StringField('student_inst_type')
    student_inst_parent = StringField('student_inst_parent')
    test_name = StringField('test_name')
    test_inst_name = StringField('test_inst_name')
    test_inst_area = StringField('test_inst_area')
    test_inst_region = StringField('test_inst_region')
    test_inst_ter = StringField('test_inst_ter')
    test_year = IntegerField('test_year')
    adapt_scale = IntegerField('adapt_scale')
    ball12 = IntegerField('ball12')
    ball100 = IntegerField('ball100')
    ball = IntegerField('ball')
    subtest = StringField('subtest')
    dpalevel = IntegerField('dpalevel')
    test_lang = StringField('test_lang')
    test_status = StringField('test_status')
    submit = SubmitField("Submit")

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

@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')


@app.route('/location_info', methods=['GET', 'POST'])
def location_info():
    columns = ("AreaName", "RegName", "TerName", "LocationID", "Delete Button")
    if db == 'postgres':
        print('This won`t be print')
        locations = get_locationinfo()[:1000]
    else:
        locations = MongoLocationInfo.info()[:1000]
        print(f'Database: {db}')
        print(locations[10])
    return render_template('location.html', columns=columns, locations=locations)


@app.route('/location_info/insert_locationinfo', methods=['POST'])
def insert_locationinfo():
    new_row = {'areaname': request.form['areaname'],
               'tername': request.form['tername'],
               'regname': request.form['regname']}
    if all([value is not None for value in new_row.values()]):
        insert_location(new_row)
    return redirect(url_for('location_info'))


@app.route('/location_info/update_locationinfo', methods=['POST'])
def update_locationinfo():
    values_on_update = {'locationid': request.form['locationid'],
                        'areaname': request.form['areaname'],
                        'tername': request.form['tername'],
                        'regname': request.form['regname']}
    if values_on_update['locationid']:
        update_location(values_on_update)        
    return redirect(url_for('location_info'))
    

@app.route('/location_info/del_location', methods=['POST'])
def del_location():
    location_id = request.form['locationid']
    delete_location(location_id)
    return redirect(url_for('location_info'))


@app.route('/institution_info', methods=['GET', 'POST'])
def institution_info():
    columns = ("InstitutionName", "LocationID", "InstitutionType", "Parent", "InstitutionID", "Delete Button")
    institutions = get_institution()[:1000]
    return render_template('institution.html', columns=columns, institutions=institutions)


@app.route('/institution_info/insert_inst', methods=['POST'])
def insert_inst():
    row_to_insert = {'instname': request.form['instname'],
                    'locationid': request.form['locationid'],
                    'insttype': request.form['insttype'],
                    'instparent': request.form['instparent']}
    if all([value is not None for value in [row_to_insert['instname'], row_to_insert['locationid']]]):
        insert_institution(row_to_insert)
    return redirect(url_for('institution_info'))


@app.route('/institution_info/update_institutioninfo', methods=['POST'])
def update_institutioninfo():
    values_on_update = {'instid': request.form['instid'],
                        'instname': request.form['instname'],
                        'locationid': request.form['locationid'],
                        'insttype': request.form['insttype'],
                        'instparent': request.form['instparent']}
    if values_on_update['instid']:
        update_institution(values_on_update)        
    return redirect(url_for('institution_info'))


@app.route('/institution_info/del_institution', methods=['POST'])
def del_institution():
    inst_Id = request.form['instid']
    delete_institution(inst_Id)
    return redirect(url_for('institution_info'))


@app.route('/student_info/insert_studentinfo', methods=['POST'])
def insert_studentinfo():
    row_to_insert =     {'outid': request.form['outid'],
                        'birth': request.form['birth'],
                        'locationid': request.form['locationid'],
                        'sextypename': request.form['sextypename'],
                        'regtypename': request.form['regtypename'],
                        'classprofilename': request.form['classprofilename'],
                        'classlangname': request.form['classlangname'],
                        'instid': request.form['instid']}
    if all([value is not None for value in [row_to_insert['outid'], row_to_insert['locationid']]]):
        insert_student(row_to_insert)
    return redirect(url_for('student_info'))


@app.route('/student_info/update_studentinfo', methods=['POST'])
def update_studentinfo():
    values_on_update = {'outid': request.form['outid'],
                        'birth': request.form['birth'],
                        'locationid': request.form['locationid'],
                        'sextypename': request.form['sextypename'],
                        'regtypename': request.form['regtypename'],
                        'classprofilename': request.form['classprofilename'],
                        'classlangname': request.form['classlangname'],
                        'instid': request.form['instid']}
    if values_on_update['outid']:
        update_student(values_on_update)        
    return redirect(url_for('student_info'))


@app.route('/student_info', methods=['GET', 'POST'])
def student_info():
    columns = ("OUTID", "Birth", "SexType", "LocationID", "StudentType", "ProfileName", "ClassLang", "InstitutionID", "Delete Button")
    students = get_student()[:1000]
    return render_template('student.html', columns=columns, students=students)


@app.route('/student_info/del_student', methods=['POST'])
def del_student():
    outid = request.form['outid']
    print(outid)
    delete_student(outid)
    return redirect(url_for('student_info'))


@app.route('/test_info/insert_testinfo', methods=['POST'])
def insert_testinfo():
    subtest = request.form['subtest']
    if subtest is not None:
        subtest = True if subtest.lower() == 'так' else False
    print(f"test subtest value: {subtest}")
    row_to_insert =     {'instid': request.form['instid'],
                        'testyear': request.form['testyear'],
                        'adaptscale': request.form['adaptscale'],
                        'ball12': request.form['ball12'],
                        'ball100': request.form['ball100'],
                        'ball': request.form['ball'],
                        'subtest': subtest,
                        'outid': request.form['outid'],
                        'testname': request.form['testname'],
                        'dpalevel': request.form['dpalevel'],
                        'testlang': request.form['testlang'],
                        'teststatus': request.form['teststatus']}
    if all([value is not None for value in [row_to_insert['instid'], row_to_insert['testyear'], row_to_insert['outid'], row_to_insert['testname']]]):
        insert_test(row_to_insert)
    return redirect(url_for('test_info'))


@app.route('/test_info', methods=['GET', 'POST'])
def test_info():
    columns = ("InstitutionID", "TestYear", "AdaptScale", "Ball12", "Ball100", "Ball", "SubTest", "OUTID", "Subject", "DPALevel",
               "Lang", "TestStatus", "TestID", "Delete Button")
    tests = get_test()[:1000]
    return render_template('test.html', columns=columns, tests=tests)


@app.route('/test_info/del_test', methods=['POST'])
def del_test():
    testId = request.form['testid']
    delete_test(testId)
    return redirect(url_for('test_info'))

@app.route('/test_info/update_testinfo', methods=['POST'])
def update_testinfo():
    subtest = request.form['subtest']
    if subtest:
        subtest = True if subtest.lower() == 'так' else False
    values_on_update = {'testid': request.form['testid'],
                        'instid': request.form['instid'],
                        'testyear': request.form['testyear'],
                        'adaptscale': request.form['adaptscale'],
                        'ball12': request.form['ball12'],
                        'ball100': request.form['ball100'],
                        'ball': request.form['ball'],
                        'subtest': subtest,
                        'outid': request.form['outid'],
                        'testname': request.form['testname'],
                        'dpalevel': request.form['dpalevel'],
                        'testlang': request.form['testlang'],
                        'teststatus': request.form['teststatus']}
    if values_on_update['testid']:
        update_test(values_on_update)        
    return redirect(url_for('test_info'))


# створити роут для вставки в базу
@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    form = UpdateTables(request.form)
    if request.method == 'POST':
    # write here maps of forms
        values = {'student_id': request.form.get("student_id"),
        'student_birth': request.form.get("student_birth"),
        'student_sex': request.form.get("student_sex"),
        'student_area': request.form.get("student_area"),
        'student_region': request.form.get("student_region"),
        'student_ter': request.form.get("student_ter"),
        'student_regtype': request.form.get("student_regtype"),
        'class_profile': request.form.get("class_profile"),
        'class_lang': request.form.get("class_lang"),
        'student_inst_name': request.form.get("student_inst_name"),
        'student_inst_area': request.form.get("student_inst_area"),
        'student_inst_region': request.form.get("student_inst_region"),
        'student_inst_ter': request.form.get("student_inst_ter"),
        'student_inst_type': request.form.get("student_inst_type"),
        'student_inst_parent': request.form.get("student_inst_parent"),
        'test_name': request.form.get("test_name"),
        'test_inst_name': request.form.get("test_inst_name"),
        'test_inst_area': request.form.get("test_inst_area"),
        'test_inst_region': request.form.get("test_inst_region"),
        'test_inst_ter': request.form.get("test_inst_ter"),
        'test_year': request.form.get("test_year"),
        'adapt_scale': request.form.get("adapt_scale"),
        'ball12': request.form.get("ball12"),
        'ball100': request.form.get("ball100"),
        'ball': request.form.get("ball"),
        'subtest': request.form.get("subtest"),
        'dpalevel': request.form.get("dpalevel"),
        'test_lang': request.form.get("test_lang"),
        'test_status': request.form.get("test_status")}

        values['subtest'] = True if values['subtest'].lower() == 'так' else False 

        insert_data(values)
        return redirect(url_for('main_page'))
    return render_template('addNew.html', form=form, action='add_data')


@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    headers = ("Рік", "Регіон", "Бал")
    result = []
    # query parameters
    form = Statistic(request.form)
    if request.method == 'POST':
        subject = request.form.getlist("subject")
        years = request.form.getlist("year")
        regions = request.form.getlist("region")
        ball_function = request.form.get("ball_function")

        print(subject)
        print(years)
        print(regions)
        if 'all' in regions:
            regions = reg_all
        result = get_statistics(years=years, regions=regions, subjects=subject, ball_function=ball_function, teststatus='Зараховано')
    return render_template('statistics.html', form=form, headers=headers, statistics_data=result)
