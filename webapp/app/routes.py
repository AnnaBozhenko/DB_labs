from flask import redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,  SelectField, SelectMultipleField
from . import app
from .models import get_statistics, get_locationinfo, insert_data, get_institution, get_student, get_test


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


class Statistic(FlaskForm):
    subjects = SelectMultipleField('subject')
    years = SelectMultipleField('year')
    regions = SelectMultipleField('region')
    ball_function = SelectField('ball_function')
    submit = SubmitField("Submit")

@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')


@app.route('/location_info', methods=['GET', 'POST'])
def location_info():
    columns = ("AreaName", "RegName", "TerName", "LocationID")
    locations = get_locationinfo()
    return render_template('location.html', columns=columns, locations=locations)


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
    columns = ("InstitutionName", "LocationID", "InstitutionType", "Parent", "InstitutionID")
    institutions = get_institution()
    return render_template('institution.html', columns=columns, institutions=institutions)


@app.route('/student_info', methods=['GET', 'POST'])
def student_info():
    columns = ("OUTID", "Birth", "SexType", "LocationID", "RegNameType", "ClassProfileName", "ClassLangName", "InstitutionID")
    students = get_student()
    return render_template('student.html', columns=columns, students=students)


@app.route('/test_info', methods=['GET', 'POST'])
def test_info():
    columns = ('instid', 'testyear', 'adaptscale', 'ball12', 'ball100', 'ball', 'subtest', 'outid', 'testname', 'dpalevel', 'testlang', 'teststatus', 'testid')
    tests = get_test()
    return render_template('test.html', columns=columns, tests=tests)

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    headers = ("Рік", "Регіон", "Предмет", "Бал")
    result = []
    # regions = []
    # subjects = []
    # years = []
    form = Statistic(request.form)
    if request.method == 'POST':
        subjects = request.form.getlist("subjects")
        years = request.form.getlist("years")
        regions = request.form.getlist("regions")
        ball_function = request.form.get("ball_function", "plain")
        if ball_function is None:
            print("ball function is None")
        else:
            result = get_statistics(years=years, regions=regions, subjects=subjects, ball_function=ball_function, teststatus='Зараховано')
    return render_template('statistics.html', headers=headers, statistics_data=result, form=form)
