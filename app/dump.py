import psycopg2
import re
import csv
import time

# --------- QUERIES ----------
query_create_insert_exams_info = """CREATE TABLE IF NOT EXISTS Insert_exams_info (
    id serial,
    year smallint,
    total_rows integer,
    wall_time numeric(10, 5),
    process_time numeric(10, 5)
    );"""

query_populate_insert_exams_info = """INSERT INTO Insert_exams_info (year, total_rows, wall_time, process_time) 
VALUES (2016, 0, 0, 0), (2017, 0, 0, 0), (2018, 0, 0, 0), (2019, 0, 0, 0), (2020, 0, 0, 0), (2021, 0, 0, 0)"""

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

# --------- VALUES ----------

db_user = "Student"
db_pass = "qwerty"
db_name = "ZNO"
db_host = "db"

loading_time = "./program_output/loading_time.txt"
query_to_db = "./program_output/queries.csv"
rows_to_write_numb = 1000
extract_data = [(2016, "./data/OpenData2016.csv", "cp1251"),
                (2017, "./data/OpenData2017.csv", "utf-8-sig"),
                (2018, "./data/OpenData2018.csv", "utf-8-sig"),
                (2019, "./data/Odata2019File.csv", "cp1251"),
                (2020, "./data/Odata2020File.csv", "cp1251"),
                (2021, "./data/Odata2021File.csv", "utf-8-sig")]

# --------- FUNCTIONALITY ----------

def construct_query_create_zno():
    columns = set()
    for year, filename, encoding in extract_data:
        with open(file=filename, encoding=encoding) as f:
            column_names = ['year'] + f.readline().strip("\n").replace("\"", "").lower().split(';')
            [columns.add(el) for el in column_names]

    columns = list(columns)
    # change order of columns to improve insertion time
    reordered_indeces = [columns.index('ukrsubtest')]
    [reordered_indeces.append(columns.index(el)) if "ball" in el else None for el in columns]
    [reordered_indeces.append(columns.index(el)) if el in ['birth', 'year'] or 'adaptscale' in el else None for el in columns]
    [reordered_indeces.append(i) if i not in reordered_indeces else None for i  in range(len(columns))]
    columns = [columns[i] for i in reordered_indeces]

    
    create_q = "CREATE TABLE IF NOT EXISTS EXAMINATIONS ("
    for col_name in columns:
        if bool(re.search('\Afr[^a]', col_name)):
            continue
        elif bool(re.search('\Asp[^a]', col_name)):
            continue
        # set type to each column
        if 'ball' in col_name:
            create_q += f"{col_name} NUMERIC(4, 1), "
        elif col_name in ['birth', 'year'] or 'adaptscale' in col_name:
            create_q += f"{col_name} SMALLINT, "
        elif col_name == 'ukrsubtest':
            create_q += f"{col_name} BOOLEAN, "
        else:
            create_q += f"{col_name} VARCHAR, "
    
    create_q = create_q[:-2] + ");"
    return create_q


def transaction(func):
    def inner(*args, **kwargs):
        conn = None
        while True:
            try:
                conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_pass)
                func(conn, *args, **kwargs)
                conn.commit()
            except psycopg2.OperationalError as ex:
                print(f"Failed to connect to database, error code: {ex.pgcode} \n {ex}")
                time.sleep(2)
            except psycopg2.DataError as ex:
                conn.rollback()
                print(f"Data error occured, error code: {ex.pgcode} \n {ex}")
                quit()
            except Exception as ex:
                conn.rollback()
                print(f"Program error occured: \n {ex}")
                quit()
            finally:
                if conn is not None:
                    conn.close()
                    break
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
    query_create_examinations = construct_query_create_zno()
    with conn.cursor() as cur:
        cur.execute(query_create_examinations)
        cur.execute(query_create_insert_exams_info)
        cur.execute("select count(*) from Insert_exams_info;")
        cur.execute(query_populate_insert_exams_info)


def set_types(column_names, values):
    for i in range(len(values)):
        if values[i] == 'null':
            values[i] = None
        elif 'ball' in column_names[i]:
            values[i] = float(values[i].replace(",", "."))
        elif column_names[i] == 'birth' or 'adaptscale' in column_names[i]:
            values[i] = int(values[i])
        elif column_names[i] == 'ukrsubtest':
            values[i] = True if values[i].lower() == 'так' else False
    return values


@transaction
def populate_examinations(conn):
    for year, filename, encoding in extract_data:
        with open(filename, encoding=encoding, newline="") as f:
            column_names = f.readline().replace("\"", "").replace("\r\n", "").lower().split(";") + ['year']
            
            for i in range(len(column_names)):
                if bool(re.search('\Afr[^a]', column_names[i])):
                    column_names[i] = 'fra' + column_names[i][2:]
                elif bool(re.search('\Asp[^a]', column_names[i])):
                    column_names[i] = 'spa' + column_names[i][2:]
            
            read_rows_n = 0
            start_wall, start_cpu = time.time(), time.process_time()
            with conn.cursor() as cur:
                cur.execute("SELECT total_rows, wall_time, process_time FROM Insert_exams_info WHERE year = %s", (year,))
                read_rows_n, passed_wall_time, passed_cpu_time = cur.fetchone()
                passed_wall_time = float(passed_wall_time)
                passed_cpu_time = float(passed_cpu_time)
                
                reader = csv.reader(f, delimiter=";")

                for _ in range(read_rows_n):
                    next(reader)
                
                counter = 0
                values_array = []
                for row in reader:
                    if counter == rows_to_write_numb:
                        try:
                            cur.execute(f"INSERT INTO Examinations ({','.join(column_names)}) VALUES {','.join(['('+','.join(['%s']*len(column_names))+')']*counter)};", values_array)
                            values_array = []
                            read_rows_n += counter
                            cur.execute("UPDATE Insert_exams_info SET total_rows = %s WHERE year = %s;", (read_rows_n, year))
                            conn.commit()
                        except psycopg2.DataError as er:
                            print(f"Error on insertion occured, error code: {er.pgcode} \n{er}")
                            conn.rollback()
                            break
                        finally:
                            counter = 0

                    row.append(year) 
                    [values_array.append(el) for el in (set_types(column_names, row))]
                    counter += 1
                
                read_rows_n += counter
                if counter > 0:
                    cur.execute(f"INSERT INTO Examinations ({','.join(column_names)}) VALUES {','.join(['('+','.join(['%s']*len(column_names))+')']*counter)};", values_array)

                end_wall, end_cpu = time.time(), time.process_time()
                passed_wall_time += end_wall - start_wall
                passed_cpu_time += end_cpu - start_cpu
                print(f"Insertion from the year {year}, process time: {passed_wall_time} seconds, cpu time: {passed_cpu_time} seconds")
                cur.execute("UPDATE Insert_exams_info SET total_rows = %s, wall_time = %s, process_time = %s where year = %s;", (read_rows_n, passed_wall_time, passed_cpu_time, year))
                conn.commit()


if __name__ == "__main__":
    prepare_tables()
    populate_examinations()
    print("Table examinations populated")
    write_time()
    write_query()
