from flask import redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,  SelectField, SelectMultipleField
from . import app
from .models import get_statistics, get_locationinfo, insert_data, get_institution, get_student, get_test, delete_location, delete_institution, delete_student, delete_test

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
    locations = get_locationinfo()
    return render_template('location.html', columns=columns, locations=locations)

@app.route('/location_info/delete', methods=['POST'])
def del_location():
    location_id = request.form['location_id']
    delete_location(location_id)
    return redirect(url_for('location_info'))


# створити роут для вставки в базу
@app.route('/add_data', methods=['GET', 'POST'])
def insert_test():
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

        insert_data(values)
        return redirect(url_for('main_page'))
    return render_template('addNew.html', form=form, action='add_data')


@app.route('/institution', methods=['GET', 'POST'])
def institution_info():
    columns = ("InstitutionName", "LocationID", "InstitutionType", "Parent", "InstitutionID", "Delete Button")
    institutions = get_institution()

    return render_template('institution.html', columns=columns, institutions=institutions)

@app.route('/institution/delete', methods=['POST'])
def del_institution():
    inst_Id = request.form['inst_Id']
    print('*****', inst_Id)
    delete_institution(inst_Id)
    return redirect(url_for('institution_info'))

@app.route('/student', methods=['GET', 'POST'])
def student_info():
    columns = ("OUTID", "Birth", "SexType", "LocationID", "StudentType", "ProfileName", "ClassLang", "InstitutionID", "Delete Button")
    students = get_student()
    return render_template('student.html', columns=columns, students=students)

@app.route('/student/delete', methods=['POST'])
def del_student():
    outid = request.form['outid']
    print(outid)
    delete_student(outid)

    return redirect(url_for('student_info'))


@app.route('/test', methods=['GET', 'POST'])
def test_info():
    columns = ("InstitutionID", "TestYear", "AdaptScale", "Ball12", "Ball100", "Ball", "SubTest", "OUTID", "Subject", "DPALevel",
               "Lang", "TestStatus", "TestID", "Delete Button")
    tests = get_test()
    return render_template('test.html', columns=columns, tests=tests)


@app.route('/test/delete', methods=['POST'])
def del_test():
    testId = request.form['testId']
    print(testId)
    delete_test(testId)
    return redirect(url_for('test_info'))

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    headers = ("Рік", "Регіон", "Предмет", "Бал")
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
            regions = []
        result = get_statistics(years=years, regions=regions, subjects=subject, ball_function=ball_function, teststatus='Зараховано')
    return render_template('statistics.html', form=form, headers=headers, statistics_data=result)
