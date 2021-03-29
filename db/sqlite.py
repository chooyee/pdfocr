import sqlite3
from sqlite3 import Error
from dotenv import load_dotenv
from infra.logger import Logger
import os

class ConMan:
    def __init__(self):
        root = os.getcwd()
        load_dotenv(root + '/config.env')
        print(os.environ.get("dbname"))
        self.database = root + '/' + os.environ.get("dbname")
        self._create_connection()
        
    def _create_connection(self):
        """ create a database connection to a SQLite database """
        self.Conn = None
        try:
            self.Conn = sqlite3.connect(self.database)
            print("Connected to " + sqlite3.version)
        except Error as e:
            print(e)
            Logger.Error(e)
            
    def _create_tables(self):
        # Create table
        con = self.Conn
        cur = con.cursor()
        cur.execute('''CREATE TABLE if not exists "conlist" (
            "id"	INTEGER,
            "uuid"	TEXT,
            "listdate"	TEXT,
            "bankname"	TEXT,
            "bankaccno"	TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        )''')
        con.commit()
    
    def Execute(self, sql, params):
        try:
            con = self.Conn
            cur = con.cursor()
            if (type(params) is list):
                cur.executemany(sql, params)
            else:
                cur.execute(sql, params)
            con.commit()
        except Exception as e:
            print("Oops!", str(e), "occurred.")
            Logger.Error(str(e))

    def Select(self, sql, params):
        print(type(params))
        try:
            con = self.Conn
            cur = con.cursor()
            cur.execute(sql, params)
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print("Select: ", str(e))
            print("Sql: ", sql)
            print("Params: ", params)
            Logger.Error("Select: " + str(e))
            Logger.Error("sql: " + sql )
            Logger.Error("Params: " + params )
            return []
   
    def Close_connection(self):
        if self.Conn:
            self.Conn.close() 

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('Disconneting from DB')
        self.Close_connection()

# with ConMan() as dbConn:
#     dbConn.method()