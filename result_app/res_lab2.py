import psycopg2
import csv
import time


task_14 = """SELECT regname, ROUND(AVG(test.ball100)::NUMERIC, 2), testyear 
FROM test 
INNER JOIN student ON test.outid = student.outid 
INNER JOIN locationinfo ON locationinfo.locationid = student.locationid
WHERE test.testname = 'Англійська мова'
AND test.teststatus = 'Зараховано'
AND test.testyear IN (2019, 2020)
GROUP BY testyear, regname;
"""


task_3 = """SELECT regname, MIN(ball100), testyear 
FROM test 
INNER JOIN student ON test.outid = student.outid 
INNER JOIN locationinfo ON locationinfo.locationid = student.locationid
WHERE test.testname = 'Українська мова і література'
AND test.teststatus = 'Зараховано'
AND test.testyear IN (2020, 2021)
GROUP BY testyear, regname;
"""

query_to_db_14 = "./result_output/result_14.csv"
query_to_db_3 = "./result_output/result_3.csv"

db_user = "Student"
db_pass = "qwerty"
db_name = "ZNO"
db_host = "db"
db_port = '5432'


def connected(username, password, database, host, port):
    while True:
        try:
            conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)
            print('Connected!!')
            return conn
        except:
            print('Trying to connect to database ... again..')
            time.sleep(5)


def main(query, file):
    conn = connected(db_user, db_pass, db_name, db_host, db_port)
    with conn.cursor() as cur:
        cur.execute(query)
        fields = [x[0] for x in cur.description]
        with open(file, 'w', encoding='windows-1251', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(fields)
            for row in cur:
                writer.writerow([str(x).replace(' ', '') for x in row])
        print('Written to the file')
    conn.close()


if __name__ == '__main__':
    try:
        main(task_14, query_to_db_14)
        main(task_3, query_to_db_3)
    except Exception as e:
        print(e)

# docker compose up result_app