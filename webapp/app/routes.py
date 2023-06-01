from flask import redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
from . import app
from .models import get_statistics, insert_into_locationInfo, get_locationinfo, insert_data

class UpdateLocation(FlaskForm):
    areaname = StringField('areaname')
    regname = StringField('regname')
    tername = StringField('tername')
    locationid = HiddenField()
    submit = SubmitField("Submit")


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')


@app.route('/location_info', methods=['GET', 'POST'])
def location_info():
    columns = ("areaname", "regname", "tername", "locationID")
    locations = get_locationinfo()
    return render_template('location.html', columns=columns, locations=locations)


@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    form = UpdateLocation(request.form)

    if request.method == 'POST':
        values = [{'areaname': request.form.get("area"), 'regname': request.form.get("region"), 'tername': request.form.get("ter")}]
        insert_into_locationInfo(values)
        return redirect(url_for('location_info'))
    return render_template('addLocation.html', form=form, action='addPlace')


# створити роут для вставки в базу 
def insert_test():
    # write here maps of forms
    values = {'student_id': student_id,
    'student_birth': student_birth,
    'student_sex': student_sex,
    'student_area': student_area,
    'student_region': student_region,
    'student_ter': student_ter,
    'student_regtype': student_regtype,
    'class_profile': class_profile,
    'class_lang': class_lang,
    'student_inst_name': student_inst_name,
    'student_inst_area': student_inst_area,
    'student_inst_region': student_inst_region,
    'student_inst_ter': student_inst_ter,
    'student_inst_type': student_inst_type,
    'student_inst_parent': student_inst_parent,
    'test_name': test_name,
    'test_inst_name': test_inst_name,
    'test_inst_area': test_inst_area,
    'test_inst_region': test_inst_region,
    'test_inst_ter': test_inst_ter,
    'test_year': test_year,
    'adapt_scale': adapt_scale,
    'ball12': ball12,
    'ball100': ball100,
    'ball': ball,
    'subtest': subtest,
    'dpalevel': dpalevel,
    'test_lang': test_lang,
    'test_status': test_status}
    insert_data(values)

    
@app.route('/institution', methods=['GET', 'POST'])
def institution_info():
    return render_template('institution.html')


@app.route('/student', methods=['GET', 'POST'])
def student_info():
    return render_template('student.html')


@app.route('/test', methods=['GET', 'POST'])
def test_info():
    return render_template("test.html", title="Test")


@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    headers = ("Рік", "Регіон", "Предмет", "Бал")
    # query parameters 
    result = get_statistics(years=[2019, 2020], regions=[], subjects=['Англійська мова'], ball_function='avg', teststatus='Зараховано')
    return render_template('statistics.html', headers=headers, statistics_data=result)
