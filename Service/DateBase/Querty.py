from ..DateBase.Connection import connection

def test():
    try:
        with connection.cursor() as cursor:
            sql_query = "SELECT * FROM typenotes;"
            cursor.execute(sql_query)
            result = cursor.fetchall()
            print(result)
    finally:
        connection.close()
        
def getUsers(data):
    try:
        with connection.cursor() as cursor:
            sql_query = "INSERT INTO `users` (`idUsers`) VALUES (%s);"
            cursor.execute(sql_query, (data['idUsers']))
            connection.commit()
            if cursor.rowcount > 0:
                return True  
            else:
                return False 
    except Exception as ex:
        print (ex)
    finally:
        connection.close()
        
def receiveNotes(data):
    try:
        with connection.cursor() as cursor:
            sql_query = "SELECT * FROM notes WHERE idUsers = %s;"
            cursor.execute(sql_query, (data['idUsers']))
            result = cursor.fetchall()
            return result
    except Exception as ex:
        print (ex)
    finally:
        connection.close()

def getNotes(data):
    try:
        with connection.cursor() as cursor:
            sql_query = "INSERT INTO `notes` (`idUsers`,`typeNotesId`,`TextNotes`,`DateNotes`) VALUES (%s , %s , %s , %s);"
            cursor.execute(sql_query, (data['idUsers'] , data['typeNotesId'] , data['TextNotes'] , data['DateNotes']))
            connection.commit()
            if cursor.rowcount > 0:
                return True  
            else:
                return False 
    except Exception as ex:
        print (ex)
    finally:
        connection.close()

def receiveNotesType(data):
    try:
        with connection.cursor() as cursor:
            sql_query = "SELECT * FROM notes WHERE idUsers = %s and typeNotesId = %s ;"
            cursor.execute(sql_query, (data['idUsers'] , data['typeNotesId']))
            result = cursor.fetchall()
            return result
    except Exception as ex:
        print (ex)
    finally:
        connection.close()

def updateNotes(data):
    try:
        with connection.cursor() as cursor:
            sql_query = "UPDATE notes SET TextNotes = %s WHERE idNotes = %s;"
            cursor.execute(sql_query, (data['TextNotes'] , data['idNotes']))
            connection.commit()
            if cursor.rowcount > 0:
                return True  
            else:
                return False 
    except Exception as ex:
        print (ex)
    finally:
        connection.close()