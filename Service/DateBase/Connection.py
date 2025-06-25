import pymysql
import pymysql.cursors

from dotenv import load_dotenv
import os
load_dotenv()
host = os.getenv('HOST')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
bd_name = os.getenv('BD_NAME')


def API(query):
    return query

try:
    connection = pymysql.connect(
    host = host,
    port = 3306,
    user = user,
    password = password,
    database = bd_name,
    cursorclass = pymysql.cursors.DictCursor
    )
    try:
        pass
    finally:
        connection.close()
except Exception as ex:
    print (ex)
    
