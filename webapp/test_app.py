from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, select, create_engine

# db_user = "postgres"
# db_pass = "1111"
# db_name = "test"
# db_host = "localhost"
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os.path
from sqlalchemy import MetaData, Table, select, create_engine


# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy()
# create the app
app = Flask(__name__, template_folder='app//templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1111@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# initialize the app with Flask-SQLAlchemy
db.init_app(app)

metadata_obj = MetaData()
engine = create_engine('postgresql+psycopg2://postgres:1111@localhost/test')
LocationInfo = Table("locationinfo", metadata_obj, autoload_with=engine, schema="public")
query_locations = select(LocationInfo)
with engine.connect() as conn:
    locations = conn.execute(query_locations).all()

# class Location(db.Model):
#    __tablename__ = 'locationinfo'
#    areaname = db.Column(db.String, nullable=False)
#    regname = db.Column(db.String, nullable=False)
#    tername = db.Column(db.String, nullable=False)
#    locationid = db.Column(db.Integer, primary_key=True)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')




@app.route('/location_info/', methods=['GET', 'POST'])
def location_info():
    columns = ("areaname", "regname", "tername", "locationID")
    # try:
    #     db.session.commit()
    #     locations = db.session.execute(db.select(Location).order_by(Location.locationid)).scalars()
    #     location_text = '<ul>'
    #     for location in locations:
    #         print(location)
    #         print(location.areaname)
    #         print(location.regname)
    #         print(location.tername)
    #         print(location.locationid)
    #         location_text += '<li>' + location.areaname + ', ' + location.regname + ', '+ location.tername + ', '  + str(location.locationid) + '</li>'
    #     location_text += '</ul>'
    #     print(location_text)
    #     return location_text
    # except Exception as e:
    #     # e holds description of the error
    #     error_text = "<p>The error:<br>" + str(e) + "</p>"
    #     hed = '<h1>Something is broken.</h1>'
    #     return hed + error_text
    print(len(locations))
    return render_template('location.html',columns=columns, locations=locations)


@app.route('/institution_info/', methods=['GET', 'POST'])
def institution_info():
    return render_template('institution.html')


@app.route('/student_info/', methods=['GET', 'POST'])
def student_info():
    return render_template('student.html')


@app.route('/test_info/', methods=['GET', 'POST'])
def test_info():
    return render_template('test.html')


@app.route('/statistics_info/', methods=['GET', 'POST'])
def statistics():
    return render_template("statistics.html", title="Queries")

if __name__ == "__main__":
    app.run(debug=True)