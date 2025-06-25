from Connection import connection

def getUsers(data):
    with connection.cursor() as cursor:
        sql_query = "INSERT INTO `users` (`idUsers`) VALUES (%s);"
        cursor.execute(sql_query, (data['idUsers']))
        connection.commit()