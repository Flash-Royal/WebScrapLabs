from getpass import getpass
from mysql.connector import connect, Error
import parse
import parseLearn

userName = 'root'
userPassword = '1234'

def textD():
    try:
        with connect(
            host = "localhost",
            user = userName,
            password = userPassword,
        ) as connection:
            createDataBase = """create database if not exists ips2"""
            useDataBase = """use ips2"""
            createTable = """create table if not exists Texts(textD text)"""
            with connection.cursor() as cur:
                cur.execute(createDataBase)
                cur.execute(useDataBase)
                cur.execute(createTable)
                connection.commit()
        with connect(
            host = "localhost",
            user = userName,
            password = userPassword,
            database = "ips2",
        ) as connection:
            eventsTable = """
                select textD from ips2.Texts
            """

            truncateTable = """
                truncate table ips2.Texts
            """
            with connection.cursor() as cur:
                cur.execute(truncateTable)
                connection.commit()
            for text in parse.texts:
                insertNewText = """
                    insert into ips2.Texts(textD)
                    values ("{0}")
                """.format(text)
                with connection.cursor() as cur:
                    cur.execute(insertNewText)
                    connection.commit()

            with connection.cursor() as cur:
                cur.execute(eventsTable)
                result = cur.fetchall()
                # for row in result:
                    # print(row)
        return result
    except Error as e:
        print(e)


result = textD()
for row in result:
    print(row)
