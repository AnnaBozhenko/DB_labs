from flask import render_template, url_for
from app import app

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html", title="Home")

@app.route('/location', methods=['GET', 'POST'])
def location():
    return render_template("location.html", title="Location")

@app.route('/student', methods=['GET', 'POST'])
def student():
    return render_template("student.html", title="Student")

@app.route('/institution', methods=['GET', 'POST'])
def institution():
    return render_template("institution.html", title="Institution")

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template("test.html", title="Test")

@app.route('/queries', methods=['GET', 'POST'])
def queries():
    return render_template("queries.html", title="Queries")

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    return render_template("statistics.html", title="Statistics")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
