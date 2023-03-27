# Adam Kennedy
# 16/03/2023
# Advanced Higher Project

from mysql.connector import connect
import sys

# class to handle database server
class MySQLServer:
    # initialises the class
    def __init__(self, app, host, user, password):
        self.app = app
        self.host = host
        self.user = user
        self.password = password
        self.ConnectToServer()

    # gets the connection to database server. NOT DATABASE.
    def ConnectToServer(self):
        try:
            self.dbConnection = connect\
                (host=self.host, user=self.user, password=self.password)
            self.cursor = self.dbConnection.cursor()
        except:
            print("Database for leaderboard was unable to be found. Have you started the database server?")
            sys.exit()

    
    # used to create new database in server
    #  and makes sure it doesn't already exist
    def CreateDB(self, databaseName):
        databaseExists = False
        self.cursor.execute("SHOW DATABASES")

        for database in self.cursor:
            if (database[0] == databaseName):
                databaseExists = True

        if not(databaseExists):
            self.cursor.execute\
                (f'CREATE DATABASE {databaseName}')
            return True
        return False
    
    # used to pick which database to use
    def UseDB(self, databaseName):
        self.cursor.execute(f'USE {databaseName}')
        return self.cursor
    
    # used to create tables
    def CreateTable(self, statement):
        self.cursor.execute(f'{statement}')
        return self.cursor
    
    # used to select from table
    def SelectStatement(self, statement):
        self.cursor.execute(f'{statement}')
        return self.cursor

    # useed to insert values into table
    def InsertStatement(self, statement):
        self.cursor.execute(f'{statement}')
        return self.cursor
    
    # used to update the table
    def UpdateStatement(self, statement):
        self.cursor.execute(f'{statement}')
        return self.cursor
    
    # used to delete records from the table
    def DeleteStatement(self, statement):
        self.cursor.execute(f'{statement}')
        return self.cursor
    