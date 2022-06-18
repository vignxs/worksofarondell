from configparser import ConfigParser
from database import Database

def create_connection_str():

    configpath = 'C:\\Users\\hrint\\Documents\\Python2022\\healthcare\\db\\config.ini'
    config = ConfigParser()
    config.read(configpath)
    insert = config.get('Json Insert', 'query')
    select = config.get('Select Query', 'query')
    dbstr = f"""dbname = {config.get('DB CREDS', 'database')} host = {config.get('DB CREDS', 'host')} port = {config.get('DB CREDS', 'port')} user = {config.get('DB CREDS', 'user')} password = {config.get('DB CREDS', 'password')}"""
        
    return dbstr, select, insert



dbstr, select, insert = create_connection_str()
infile = open(r'C:/Users/hrint/Documents/Python2022/healthcare/data.json', 'r', encoding = 'utf-8')
json_data = infile.read()

query = 'insert into referral_info select * from json_populate_recordset(NULL::reffreral_info, %s)'




with Database(connstr = dbstr) as db:
    db.execute(insert, (json_data,))
   