import mysql.connector
from datetime import date, datetime, timedelta
import pandas as pd

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
    def tableHasData(self,table) -> bool:
        try:
            db = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.passw,
            )

            cursor = db.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM userdb.{table}")
            count = cursor.fetchone()[0]

            cursor.close()
            db.close()

            if count > 0:
                return 1  # van adat
            else:
                return 0  # nincs adat

        except Exception as e:
            print(f"Error: {e}")
            return 0

    def cooling_panels_df_to_db(self, df):
        import mysql.connector

        try:
            db = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.passw
            )
            cursor = db.cursor()

            sql = """
            INSERT INTO userdb.cooling_panels (panel_id, panel_name)
            VALUES (%s, %s)
            """

            values = [
                (int(r.panel_id), r.panel_name)
                for r in df.itertuples(index=False)
            ]

            cursor.executemany(sql, values)
            db.commit()

        except mysql.connector.Error as e:
            print(f"MySQL hiba: {e}")
            db.rollback()

        finally:
            cursor.close()
            db.close()

    def measurement_data_df_to_db(self, df):
        import mysql.connector

        try:
            db = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.passw
            )
            cursor = db.cursor()

            sql = """
            INSERT INTO userdb.measurement_data (panel_id, timestamp, temperature_c)
            VALUES (%s, %s, %s)
            """

            values = [
                (int(r.panel_id), r.timestamp, float(r.temperature_c))
                for r in df.itertuples(index=False)
            ]

            cursor.executemany(sql, values)
            db.commit()

        except mysql.connector.Error as e:
            print(f"MySQL hiba: {e}")
            db.rollback()

        finally:
            cursor.close()
            db.close()

    def portions_df_to_db(self, df):
        import mysql.connector

        try:
            db = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.passw
            )
            cursor = db.cursor()

            sql = """
            INSERT INTO userdb.doses (dose_id, start_date, start_time, end_date, end_time, interval_sec, duration_min)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            values = [
                (int(r.dose_id), r.start_date, r.start_time, r.end_date, r.end_time, r.interval_sec, r.duration_min)
                for r in df.itertuples(index=False)
            ]

            cursor.executemany(sql, values)
            db.commit()

        except mysql.connector.Error as e:
            print(f"MySQL hiba: {e}")
            db.rollback()

        finally:
            cursor.close()
            db.close()