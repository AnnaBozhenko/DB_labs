from flask import render_template, url_for
from webapp.app import app

@app.route('/')
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
    return render_template('test.html')


@app.route('/queries', methods=['GET', 'POST'])
def queries():
    return render_template("queries.html", title="Queries")

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    return render_template("statistics.html", title="Statistics")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
