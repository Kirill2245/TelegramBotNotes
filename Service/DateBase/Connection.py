import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os



def get_db_connection():
    load_dotenv()
    host = os.getenv('HOST')
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    bd_name = os.getenv('BD_NAME')

    config = {
    "host": host,  
    "user": user,     
    "password": password,  
    "database": bd_name
    }
    try:
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print("✅ Успешное подключение к MySQL!")
            return connection
        else:
            print(f"❌ Ошибка подключения")
    except Error as e:
        print(f"❌ Ошибка подключения: {e}")
