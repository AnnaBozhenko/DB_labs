import psycopg2
import csv
import time
from generate_queries import *

# --------- VALUES ----------

db_user = "postgres"
db_pass = "turtle"
db_name = "python_db"
db_host = "localhost"

rows_to_write_numb = 100
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
        f.write(content + '\n')


def get_type(name):
    """name - str;
    returns str, representing the sql data type of the given column 'name'."""
    name = name.lower()
    if "ball" in name:
        return "numeric(4, 1)"
    elif name == "ukrsubtest":
        return "boolean"
    elif any([name == el for el in ["ukradaptscale", "birth", "testyear"]]):
        return "smallint"
    else:
        return "varchar"


def format_value(column_name):
    """column_name - str;
    returns function to typecast value, which belongs to the column column_name."""
    column_name = column_name.lower()
    if "ball" in column_name:
        return lambda x: x.replace(",", ".")
    elif column_name == "ukrsubtest":
        return lambda x: x if x == "null" else "true" if x.lower() =="так" else "false"
    elif any([column_name == el for el in ["ukradaptscale", "birth", "testyear"]]):
        return lambda x: x
    else:
        return lambda x: "\'" + x.replace("'", "''") + "\'"  if x != "null" else "null"


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
    sorted_columns_types = ", ".join([c_name + " " + c_type for c_name, c_type in sorted_columns_types])

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
                rows = [row + [str(year)] for row in [next(reader, None) for _ in range(rows_to_write_numb)] if row is not None]
                # format each rows' values to sql-standart to perform insert, encoding each string to utf-8
                rows = [[f(x) for f, x in zip(formatters, row)] for row in rows]
                values = ", ".join(["(" + ", ".join(row) + ")" for row in rows])
                query = f"INSERT INTO Examinations ({', '.join(column_names)}) VALUES {values};"
                cur.execute(query)


@transaction
def migrate(conn):
    with conn.cursor() as cur:
        cur.execute(q_create_locationInfo())     
        cur.execute(create_index_on_locationinfo())  
        cur.execute(q_create_institution())        
        cur.execute(q_create_student_1())            
        cur.execute(q_create_student_2())             
        cur.execute(q_create_student_3())             
        cur.execute(q_create_student_4())             
        cur.execute(q_create_test_1())              
        cur.execute(q_create_test_2())               
        cur.execute(q_clean_unnecessary_structures())


if __name__ == "__main__":
    prepare_tables()
    print('Table is prepared')
    populate_examinations()
    print("Table examinations populated")
    migrate()
    print("Migrations script generated")
