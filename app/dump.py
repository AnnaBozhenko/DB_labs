import psycopg2
import csv
import time
from generate_queries import *

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
 	where examinations.testyear = 2020 and ukrteststatus = 'Зараховано'
	group by regname) as statistics2020
join 
(select 
	regname,
 	min(ukrball100) as min_ball_100_from_2021
	from examinations 
 	where examinations.testyear = 2021 and ukrteststatus = 'Зараховано'
	group by regname) as statistics2021
using(regname);"""

query_create_insert_log = """create table if not exists InsertLog (
    year smallint primary key,
    inserted_rows_n integer,
    insertion_time numeric(10, 5)
);"""

# --------- VALUES ----------

db_user = "Student"
db_pass = "qwerty"
db_name = "ZNO"
db_host = "db"

loading_time = "./program_output/loading_time.txt"
query_to_db = "./program_output/queries.csv"
baseline_name = "./flyway/sql/V1__initial_schema.sql"
migrations_name ="./flyway/sql/V2__migrations.sql"

rows_to_write_numb = 1000
DB_POPULATED = False
extract_data = [(2016, "./data/OpenData2016.csv", "cp1251"),
                (2017, "./data/OpenData2017.csv", "utf-8-sig"),
                (2018, "./data/OpenData2018.csv", "utf-8-sig"),
                (2019, "./data/Odata2019File.csv", "cp1251"),
                (2020, "./data/Odata2020File.csv", "cp1251"),
                (2021, "./data/Odata2021File.csv", "utf-8-sig")]

# --------- FUNCTIONALITY ----------
def write_to_file(file_path, content):
    """file_path - str, path of file to write to;
    content - str, content to write to file.
    returns nothing, writes content to file."""
    with open(file_path, mode="a") as f:
        f.write('\n' + content + '\n')


def get_type(name):
    """name - str;
    returns str, representing the sql data type of the given column 'name'."""
    name = name.lower()
    if "ball" in name:
        return "numeric(4, 1)"
    elif name == "ukrsubtest":
        return "boolean"
    elif any([name == el for el in["ukradaptscale", "birth", "testyear"]]):
        return "smallint"
    else:
        return "varchar"


def format_value(column_name):
    """column_name - str;
    returns function to typecast value, which belongs to the column column_name."""
    column_name = column_name.lower()
    if "ball" in column_name:
        return lambda x: float(x.replace(",", ".")) if x != "null" else None
    elif column_name == "ukrsubtest":
        return lambda x: None if x == "null" else True if x.lower() =="так" else False
    elif any([column_name == el for el in ["ukradaptscale", "birth", "testyear"]]):
        return lambda x: int(x) if x != "null" else None
    else:
        return lambda x: x if x != "null" else None


def format_column(name):
    """name - unformatted string, representing column name;
    returns formatted to standart column name."""
    name = name.lower()
    name = name[:2] + name[3:] if len(name) > 3 and (name[:3] == 'fra' or name[:3] == 'spa') else name
    return name 


def get_query_create_examinations():
    """returns string, a query to create table Examinations"""
    columns_names = []
    for year, filename, encoding in extract_data:
        with open(filename, encoding=encoding) as f:
            reader = csv.reader(f, delimiter=";")
            columns_names += [format_column(el) for el in next(reader)]    

    columns_types = [(el, get_type(el)) for el in set(columns_names + ["testyear"])]
    sorted_columns_types = []
    for type in ["boolean", "smallint", "numeric(4, 1)", "varchar"]:
        [sorted_columns_types.append((c_name, c_type)) for c_name, c_type in columns_types if c_type == type]
    sorted_columns_types = ", ".join([c_name +" "+ c_type for c_name, c_type in sorted_columns_types])

    query = "CREATE TABLE IF NOT EXISTS Examinations (" + sorted_columns_types + ");"
    return query


def transaction(func):
    """wrapper function for functions which use connection sessions to postgres"""
    def inner(*args, **kwargs):
        conn = None
        while True:
            try:
                conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_pass)
                result = func(conn, *args, **kwargs)
                conn.commit()
                return result
            except psycopg2.OperationalError as ex:
                print(f"Failed to connect to database\n {ex}")
                time.sleep(2)
            except psycopg2.DataError as ex:
                conn.rollback()
                print(f"Data error occured\n {ex}")
                quit()
            except Exception as ex:
                conn.rollback()
                print(f"Program error occured: \n {ex}")
                quit()
            finally:
                if conn is not None:
                    conn.close()
    return inner


@transaction
def write_time(conn):
    """conn - psycopg2 Connection object;
    the function writes total database load time to file."""
    with conn.cursor() as cur:
        cur.execute("SELECT SUM(insertion_time) FROM InsertLog;")
        wall_time = cur.fetchone()[0]
        with open(loading_time, 'w') as f:
            f.write(f"total wall time: {wall_time} seconds\n")
        

@transaction
def write_query(conn):
    """conn - psycopg2 Connection object;
    the function performs given query to database and in case of receiving the result writes it to the file."""
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
    """conn - psycopg2 Connection object;
    the function:
        - creates tables neccessary for database: 
            - examination table (examinations' data);
            - insertlog table (information on insert to examinations table: 
            number of rows inserted and total insertion time for specific year),
        - populates insertlog table with default initial rows, where each row corresponds to each year insert info.
    returns true in case of complete database population."""
    query_create_exams = get_query_create_examinations()
    
    with conn.cursor() as cur:
        cur.execute(query_create_exams)
        write_to_file(baseline_name, query_create_exams)
        cur.execute(query_create_insert_log)
        write_to_file(baseline_name, query_create_insert_log)
        cur.execute("select count(*) from insertlog;")
        if cur.fetchone()[0] == 0:
            query = cur.mogrify(f"insert into InsertLog (year, inserted_rows_n, insertion_time) values {', '.join(['%s']*len(extract_data))}", [(info[0], 0, 0) for info in extract_data])
            cur.execute(query)
            write_to_file(baseline_name, query.decode())


@transaction
def populate_examinations(conn):
    """conn - psycopg2 Connection object;
    the function populates the given database into the conn object,
    returns true in case of successful population."""
    for year, filename, encoding in extract_data:
        with open(filename, encoding=encoding) as f:
            reader = csv.reader(f, delimiter=";")
            column_names = next(reader) + ['testyear']
            column_names = [format_column(el) for el in column_names] 
            formatters = [format_value(c) for c in column_names]
                        
            with conn.cursor() as cur:
                start_time = time.time()
                cur.execute(f"SELECT inserted_rows_n FROM InsertLog where year = {year};")
                read_rows_n = cur.fetchone()[0]
                
                [next(reader) for _ in range(read_rows_n)]
                
                while True:
                    rows = [row + [year] for row in [next(reader, None) for _ in range(rows_to_write_numb)] if row is not None]
                    rows_n = len(rows)
                    if rows_n > 0:
                        rows = [tuple([f(x) for f, x in zip(formatters, row)]) for row in rows]
                        
                        query = cur.mogrify(f"INSERT INTO Examinations ({', '.join(column_names)}) VALUES {', '.join(['%s']*rows_n)};", rows)
                        cur.execute(query)
                        write_to_file(baseline_name, query.decode())

                        cur.execute("select inserted_rows_n, insertion_time FROM InsertLog where year = %s;", (year,))
                        total_rows, insertion_time = cur.fetchone()
                        total_rows += rows_n
                        insertion_time = float(insertion_time) + time.time() - start_time
                        query = cur.mogrify("UPDATE InsertLog SET inserted_rows_n = %s, insertion_time = %s WHERE year = %s;", (total_rows, insertion_time, year))
                        cur.execute(query)
                        write_to_file(baseline_name, query.decode())
                        conn.commit()

                        start_time = time.time()
                    else:
                        break


if __name__ == "__main__":
    prepare_tables()
    populate_examinations()
    print("Table examinations populated")
    write_time()
    write_query()
    write_to_file(migrations_name, q_create_locationInfo())
    write_to_file(migrations_name, q_create_institution())
    write_to_file(migrations_name, q_create_student())
    write_to_file(migrations_name, q_create_test())
    query = """
drop table examinations;
drop table insertLog;
"""
    write_to_file(migrations_name, query)
    print("Migrations script generated")
