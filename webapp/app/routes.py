from flask import render_template
from . import app
from .models import get_statistics

@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')

@app.route('/location', methods=['GET', 'POST'])
def location_info():
    return render_template('location.html')


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
