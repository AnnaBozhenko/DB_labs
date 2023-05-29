from flask import render_template, url_for
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Home")

@app.route('/location')
def location():
    return render_template("location.html", title="Location")

@app.route('/student')
def student():
    return render_template("student.html", title="Student")

@app.route('/institution')
def institution():
    return render_template("institution.html", title="Institution")

@app.route('/test')
def test():
    return render_template("test.html", title="Test")

@app.route('/queries')
def queries():
    return render_template("queries.html", title="Queries")
