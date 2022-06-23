from configparser import ConfigParser
from database import Database
from checks import Checkups
def create_connection_str():

    configpath = 'C:\\Users\\hrint\\Documents\\Python2022\\healthcare\\db\\config.ini'
    config = ConfigParser()
    config.read(configpath)
    insert = config.get('Json Insert', 'query')
    select = config.get('Select Query', 'query')
    dbstr = f"""dbname = {config.get('DB CREDS', 'database')} host = {config.get('DB CREDS', 'host')} port = {config.get('DB CREDS', 'port')} user = {config.get('DB CREDS', 'user')} password = {config.get('DB CREDS', 'password')}"""
        
    return dbstr, select, insert

checks = Checkups()
print(checks)
f = ('C:/Users/hrint/Documents/Python2022/healthcare/db/data.json')
checks.prime_checks(f)

# dbstr, select, insert = create_connection_str()
# infile = open(r'C:/Users/hrint/Documents/Python2022/healthcare/db/data.json', 'r', encoding = 'utf-8')
# json_data = infile.read()

# with Database(connstr = dbstr) as db:
#     db.execute(insert, (json_data,))
   