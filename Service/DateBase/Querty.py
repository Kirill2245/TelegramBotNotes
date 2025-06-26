from ..DateBase.Connection import get_db_connection

# def test():
#     try:
#         with connection.cursor() as cursor:
#             sql_query = "SELECT * FROM typenotes;"
#             cursor.execute(sql_query)
#             result = cursor.fetchall()
#             print(result)
#     finally:
#         connection.close()
  
def getUsers(data):
    print("getUsers")
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql_query = "INSERT INTO `users` (`idUsers`) VALUES (%s);"
            cursor.execute(sql_query, (data['idUsers'],))
            connection.commit()
            if cursor.rowcount > 0:
                return True  
            else:
                return False 
    except Exception as ex:
        print(ex)
    finally:
        if connection:  # Закрываем только если было открыто
            connection.close()
        
def receiveNotes(data):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql_query = "SELECT * FROM notes WHERE idUsers = %s;"
            cursor.execute(sql_query, (data['idUsers'],))
            result = cursor.fetchall()
            return result
    except Exception as ex:
        print(ex)
    finally:
        if connection:  # Закрываем только если было открыто
            connection.close()

def getNotes(data):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql_query = "INSERT INTO `notes` (`idUsers`,`typeNotesId`,`TextNotes`,`DateNotes`) VALUES (%s , %s , %s , %s);"
            cursor.execute(sql_query, (data['idUsers'] , data['typeNotesId'] , data['TextNotes'] , data['DateNotes'],))
            connection.commit()
            if cursor.rowcount > 0:
                return True  
            else:
                return False 
    except Exception as ex:
        print(ex)
    finally:
        if connection:  # Закрываем только если было открыто
            connection.close()

def receiveNotesType(data):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql_query = "SELECT * FROM notes WHERE idUsers = %s and typeNotesId = %s ;"
            cursor.execute(sql_query, (data['idUsers'] , data['typeNotesId'],))
            result = cursor.fetchall()
            return result
    except Exception as ex:
        print(ex)
    finally:
        if connection:  # Закрываем только если было открыто
            connection.close()

def updateNotes(data):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql_query = "UPDATE notes SET TextNotes = %s WHERE idNotes = %s;"
            cursor.execute(sql_query, (data['TextNotes'] , data['idNotes'],))
            connection.commit()
            if cursor.rowcount > 0:
                return True  
            else:
                return False 
    except Exception as ex:
        print(ex)
    finally:
        if connection:  # Закрываем только если было открыто
            connection.close()

def delateNotes(data):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql_query = "DELETE FROM notes WHERE idNotes = %s"
            cursor.execute(sql_query, (data['idNotes'],))
            connection.commit()
            if cursor.rowcount > 0:
                return True  
            else:
                return False 
    except Exception as ex:
        print(ex)
    finally:
        if connection:  # Закрываем только если было открыто
            connection.close()
        
def searchNotes(data):
    search_text = f"%{data['TextNotes']}%"
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql_query = "SELECT * FROM notes WHERE idUsers = %s and TextNotes LIKE %s;"
            cursor.execute(sql_query, (data['idUsers'] , search_text))
            result = cursor.fetchall()
            return result
    except Exception as ex:
        print(ex)
    finally:
        if connection:  # Закрываем только если было открыто
            connection.close()

def checkUsers(data):
    print("checkUsers")
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql_query = "SELECT COUNT(*) AS user_count FROM users WHERE idUsers = %s;"
            cursor.execute(sql_query, (data['idUsers'],))
            result = cursor.fetchone()
            user_count = result[0] 
            return user_count > 0
    except Exception as ex:
            print(ex)
    finally:
        if connection:  # Закрываем только если было открыто
            connection.close()

