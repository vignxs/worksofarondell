import psycopg2 as pg
from configparser import ConfigParser
import os
import json


class Database:
    def __init__(self, connstr):
        self._conn = pg.connect(connstr)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()



if __name__ == "__main__":

    configpath = 'C:\\Users\\hrint\\Documents\\Python2022\\healthcare\\db\\config.ini'
    config = ConfigParser()

    # if os.path.exists(configpath):
    config.read(configpath)

    host = config.get('DB CREDS', 'host')
    port = config.get('DB CREDS', 'port')
    user = config.get('DB CREDS', 'user')
    password = config.get('DB CREDS', 'password')
    database = config.get('DB CREDS', 'database')

    for key, values in config['DB CREDS'].items():
        print(key, values)

    dbstr = f'dbname = {database} host = {host} port = {port} user = {user} password = {password}'

    print(dbstr)
    # infile = open(r'C:/Users/hrint/Documents/Python2022/healthcare/data.json', 'r', encoding = 'utf-8')
    # json_data = infile.read()
    # query_sql = """ insert into reffreral_info select * from json_populate_record(NULL::reffreral_info, %s) """


    
    # with Database(connstr= dbstr) as db:
    #     db.execute(query_sql, (json_data,))