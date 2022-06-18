import psycopg2 as pg
import json

f = open(r'C:/Users/hrint/Documents/Python2022/healthcare/data.json', 'r', encoding = 'utf-8')
json_data = f.read()
try:
    conn = pg.connect("dbname = 'healthcare'  host = 'localhost' user = 'postgres' password = '12345'")
    if conn:
        conn.autocommit = True
        cursr = conn.cursor()

        query_sql = """ insert into reffreral_info select * from json_populate_record(NULL::reffreral_info, %s) """
        cursr.execute(query_sql, (json_data,))

except Exception as e:
    print(e)

finally:
    conn.close()


#with pg.connect :
    # conn = pg.connect(database = 'healthcare',  host = 'localhost', user = 'postgres', password = '12345')
#with pg.connect string:
    # conn = pg.connect("dbname = 'healthcare'  host = 'localhost' user = 'postgres' password = '12345'")