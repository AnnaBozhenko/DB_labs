from flask import redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,  SelectField, SelectMultipleField
from . import app
from .models import get_statistics, get_locationinfo, insert_data, get_institution, get_student, get_test, delete_location, delete_institution, delete_student, delete_test

class UpdateLocation(FlaskForm):
    areaname = StringField('areaname')
    regname = StringField('regname')
    tername = StringField('tername')
    locationid = HiddenField()
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
    locations = get_locationinfo()
    return render_template('location.html', columns=columns, locations=locations)

@app.route('/location_info/delete', methods=['POST'])
def del_location():
    location_id = request.form['location_id']
    delete_location(location_id)
    return redirect(url_for('location_info'))


# створити роут для вставки в базу 
def insert_test():
    {'student_id'
    'student_birth'
    'student_sex'
    'student_area'
    'student_region'
    'student_ter'
    'student_regtype'
    'class_profile'
    'class_lang'
    'student_inst_name'
    'student_inst_area'
    'student_inst_region'
    'student_inst_ter'
    'student_inst_type'
    'student_inst_parent'

    'test_name'
    'test_inst_name'
    'test_inst_area'
    'test_inst_region'
    'test_inst_ter'
    'test_year'
    'adapt_scale'
    'ball12'
    'ball100'
    'ball'
    'subtest'
    'dpalevel'
    'test_lang'
    'test_status'}
    


@app.route('/institution', methods=['GET', 'POST'])
def institution_info():
    columns = ("InstitutionName", "LocationID", "InstitutionType", "Parent", "InstitutionID", "Delete Button")
    institutions = get_institution()[:1000]

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
    students = get_student()[:1000]
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
    tests = get_test()[:1000]
    return render_template('test.html', columns=columns, tests=tests)


@app.route('/test/delete', methods=['POST'])
def del_test():
    testId = request.form['testId']
    print(testId)
    delete_test(testId)
    return redirect(url_for('test_info'))

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
        if len(result) > 1000:
            result = result[:1000]
    return render_template('statistics.html', form=form, headers=headers, statistics_data=result)
