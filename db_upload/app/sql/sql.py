import mysql.connector
from datetime import date, datetime, timedelta

class Database():
    def __init__(self,host:str, port:int, user:str, passw:str):
        self.host = host
        self.port = port
        self.user = user
        self.passw = passw

    def isRdy(self)->bool:
        try:
            db = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.passw)

            db.close()
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 0
