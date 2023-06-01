from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, select, create_engine, desc
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
import os
SECRET_KEY = os.urandom(32)


# db_user = "postgres"
# db_pass = "1111"
# db_name = "test"
# db_host = "localhost"




# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy()
# create the app
app = Flask(__name__, template_folder='app//templates', static_folder='app//static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1111@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = SECRET_KEY

# initialize the app with Flask-SQLAlchemy
db.init_app(app)
metadata_obj = MetaData()
engine = create_engine('postgresql+psycopg2://postgres:1111@localhost/test')
LocationInfo = Table("locationinfo", metadata_obj, autoload_with=engine, schema="public")

query_locations = select(LocationInfo).order_by(desc(LocationInfo.c.locationid))



class UpdateLocation(FlaskForm):
    areaname = StringField('areaname')
    regname = StringField('regname')
    tername = StringField('tername')
    submit = SubmitField("Submit")

def get_db_session_scope(sql_db_session):
    session = sql_db_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')




@app.route('/location_info/', methods=['GET', 'POST'])
def location_info():


    with engine.connect() as conn:
        locations = conn.execute(query_locations).all()
    columns = ("areaname", "regname", "tername", "locationID")

    return render_template('location.html', columns=columns, locations=locations)


@app.route('/add_location/', methods=['GET', 'POST'])
def add_location():
    form = UpdateLocation(request.form)

    if request.method == 'POST':
        area = request.form.get("area")
        region = request.form.get("region")
        ter = request.form.get("ter")

        new_location = LocationInfo.insert().values(areaname=area, regname=region, tername=ter)
        print(new_location)

        with engine.connect() as conn:
            result = conn.execute(new_location)
            conn.commit()
            print(result)

        # with engine.connect() as conn:
        #     conn.execute(new_location)
        #
        # db.session.commit()
        return redirect(url_for('location_info'))
    return render_template('addLocation.html', form=form, action='addPlace')

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