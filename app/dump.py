import psycopg2
import re
import csv
import time

# Порівняти найгірший бал з Української мови та літератури у кожному регіоні у 2020 та
# 2021 роках серед тих кому було зараховано тест
comparison_query = """
select 
	regname,
	min_ball_100_from_2020,
	min_ball_100_from_2021
from
(select 
 	regname,
	min(ukrball100) as min_ball_100_from_2020
 	from examinations 
 	where examinations.year = 2020 and ukrteststatus = 'Зараховано'
	group by regname) as statistics2020
join 
(select 
	regname,
 	min(ukrball100) as min_ball_100_from_2021
	from examinations 
 	where examinations.year = 2021 and ukrteststatus = 'Зараховано'
	group by regname) as statistics2021
using(regname);"""

query_create_insert_log = """create table InsertLog (
    year smallint primary key,
    inserted_rows_n integer,
    insertion_time numeric(10, 5)
);"""

# --------- VALUES ----------
mapper_pattern_column = {"(st|out)id":         "OutId",                 
                         "birth":              "Birth", 
                         "sex.+":              "SexTypeName", 
                         "regtypename":        "RegTypeName", 
                         "tertypename":        "TerritoryTypeName",
                         "classprofile":       "ClassProfileName", 
                         "class(lang|reg)name":"ClassLangName",   
                         "eotypename":         "InstitutionType",  
                         "eoparent$":          "Parent",           
                         "(eo|.+pt)name":      "InstitutionName",
                         "(eo|.*pt)areaname":  "InstitutionAreaName", 
                         "^areaname":          "StudentAreaName",
                         "(eo|.*pt)regname":   "InstitutionRegionName",
                         "^regname":           "StudentRegionName",
                         "(eo|.*pt)tername":   "InstitutionTerritoryName",
                         "^tername":           "StudentTerritoryName",  
                         ".+test$":             "TestName",       
                         ".+lang$":            "TestLanguage",   
                         ".+ball12":           "Ball12",         
                         ".+dpalevel":         "DPAlevel",       
                         ".*adaptscale":       "AdaptScale",     
                         ".+ball$":            "Ball",           
                         ".+ball100":          "Ball100",        
                         ".+teststatus":       "TestStatus",       
                         ".*subtest":          "SubTest",
                         "year":               "TestYear"}        

mapper_pattern_test =  {"uml": "uml", 
                        "ukr": "ukr", 
                        "hist": "hist", 
                        "math[^s]": "math",
                        "mathst": "mathst", 
                        "phys": "phys",
                        "chem": "chem", 
                        "bio": "bio", 
                        "geo": "geo", 
                        "eng": "eng", 
                        "deu": "deu", 
                        "rus": "rus", 
                        "sp": "sp", 
                        "spa": "sp", 
                        "fr": "fr"}

# db_user = "Student"
# db_pass = "qwerty"
# db_name = "ZNO"
# db_host = "db"
db_user="postgres"
db_pass="turtle"
db_name="learn_examples"
db_host="localhost"

loading_time = "./program_output/loading_time.txt"
query_to_db = "./program_output/queries.csv"
ddl_commands = "./migrations/V1__create_examinations.sql"
dml_commands = "./migrations/V2__populate_examinations.sql"
create_schema = "create_schema.sql"

rows_to_write_numb = 1000
extract_data = [(2016, "./data/OpenData2016.csv", "cp1251"),
                (2017, "./data/OpenData2017.csv", "utf-8-sig"),
                (2018, "./data/OpenData2018.csv", "utf-8-sig"),
                (2019, "./data/Odata2019File.csv", "cp1251"),
                (2020, "./data/Odata2020File.csv", "cp1251"),
                (2021, "./data/Odata2021File.csv", "utf-8-sig")]

# --------- FUNCTIONALITY ----------
def get_type(name):
    name = name.lower()
    if "ball" in name:
        return "numeric(4, 1)"
    elif "subtest" in name:
        return "boolean"
    elif any([el in name for el in["adaptscale", "birth", "testyear"]]):
        return "smallint"
    else:
        return "varchar"


def format_value(column_name):
    column_name = column_name.lower()
    if "ball" in column_name:
        return lambda x: x.replace(",", ".") if x != "null" else None
    elif "subtest" in column_name:
        return lambda x: None if x == "null" else "true" if x.lower() =="так" else "false"
    else:
        return lambda x: x if x != "null" else None


def set_type(name):
    if "ball" in name:
        return lambda x: float(x)
    elif "subtest" in name:
        return lambda x: True if x.lower()=="так" else False
    elif name in "adaptscale" or name in "birth" or name in "testyear":
        return lambda x: int(x)
    else:
        return lambda x: x


def format_column(name):
    """name - unformatted string, representing column name;
    returns formatted to standart column name."""
    name = name.lower()
    for pattern, column_name in mapper_pattern_column.items():
        if bool(re.match(pattern, name)):
            test = [v for k, v in mapper_pattern_test.items() if bool(re.match(k, name))]
            test = test[0] if test != [] else ''
            return test + column_name
    raise Exception(f"Couldn't resolve name: {name}")


def get_query_create_examinations():
    """returns string, a query to create table Examinations"""
    columns_names = []
    for year, filename, encoding in extract_data:
        with open(filename, encoding=encoding) as f:
            reader = csv.reader(f, delimiter=";")
            columns_names += [format_column(el) for el in next(reader)]
    columns_types = [el + " " + get_type(el) for el in set(columns_names + ["TestYear"])]
    query = "CREATE TABLE Examinations (" + ', '.join(columns_types) + ");"
    
    return query


def transaction(func):
    def inner(*args, **kwargs):
        conn = None
        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_pass)
        func(conn, *args, **kwargs)
        conn.commit()
        conn.close()

        # while True:
        #     try:
                # conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_pass)
                # func(conn, *args, **kwargs)
                # conn.commit()
            # except psycopg2.OperationalError as ex:
            #     print(f"Failed to connect to database, error code: {ex.pgcode} \n {ex}")
            #     time.sleep(2)
            # except psycopg2.DataError as ex:
            #     conn.rollback()
            #     print(f"Data error occured, error code: {ex.pgcode} \n {ex}")
            #     quit()
            # except Exception as ex:
            #     conn.rollback()
            #     print(f"Program error occured: \n {ex}")
            #     quit()
            # finally:
            #     if conn is not None:
                    # conn.close()
                    # break
    return inner


@transaction
def write_time(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT SUM(wall_time), SUM(process_time) FROM Insert_exams_info;")
        wall_time, process_time = cur.fetchone()
        with open(loading_time, 'w') as f:
            f.write(f"total wall time: {wall_time} seconds\n")
            f.write(f"total cpu time: {process_time} seconds")
        

@transaction
def write_query(conn):
    with conn.cursor() as cur:
        cur.execute(comparison_query)
        rows = cur.fetchall()
        column_names = [el[0] for el in cur.description]
        with open(query_to_db, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(column_names)
            [writer.writerow(row) for row in rows]


@transaction
def prepare_tables(conn):
    query_create_exams = get_query_create_examinations()
    
    with conn.cursor() as cur:
        cur.execute(query_create_exams)
        cur.execute(query_create_insert_log)
        cur.execute(f"insert into InsertLog (year, inserted_rows_n, insertion_time) values {', '.join(['%s']*len(extract_data))}", [(info[0], 0, 0) for info in extract_data])


@transaction
def populate_examinations(conn):
    def insert_to_tables(y, columns, values, cur, n):
        query = f"INSERT INTO Examinations ({', '.join(columns)}) VALUES {', '.join(['%s']*len(values))};"
        cur.execute(query, values)
        cur.execute("UPDATE InsertLog SET inserted_rows_n = %s WHERE year = %s;", (n, y))
        conn.commit()

    for year, filename, encoding in extract_data:
        print(f"year: {year}")
        with open(filename, encoding=encoding) as f:
            reader = csv.reader(f, delimiter=";")
            column_names = next(reader) + ['year']
            [print(before, after) for before, after in zip(column_names, [format_column(el) for el in column_names] )]
            column_names = [format_column(el) for el in column_names] 
            formatters = [format_value(c) for c in column_names]
            
            start_wall = time.time()
            
            with conn.cursor() as cur:
                cur.execute(f"SELECT inserted_rows_n, insertion_time FROM InsertLog where year = {year};")
                read_rows_n, passed_wall_time = cur.fetchone()
                passed_wall_time = float(passed_wall_time)
                
                for _ in range(read_rows_n):
                    next(reader)
                
                counter = 0
                values_array = []
                for row in reader:
                    if counter == rows_to_write_numb:
                        read_rows_n += counter
                        insert_to_tables(year, column_names, values_array, cur, read_rows_n)
                        counter = 0

                    row.append(year) 
                    values_array.append(tuple([func(el) for func, el in zip(formatters, row)]))
                    counter += 1
                
                read_rows_n += counter
                if counter > 0:
                    insert_to_tables(year, column_names, values_array, cur, read_rows_n)
                    counter = 0

                end_wall = time.time()
                passed_wall_time += end_wall - start_wall
                print(f"Insertion from the year {year}, process time: {passed_wall_time} seconds")
                cur.execute("UPDATE InsertLog SET insertion_time = %s where year = %s;", (passed_wall_time,))
                conn.commit()


if __name__ == "__main__":
    prepare_tables()
    populate_examinations()
    print("Table examinations populated")
    # write_time()
    # write_query()
