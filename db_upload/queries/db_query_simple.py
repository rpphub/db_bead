import pymysql

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "db_bead",
    "password": "db_pass",
    "database": "userdb",
    "cursorclass": pymysql.cursors.DictCursor
}
#kapcsolat létrehozása
def get_connection():
    return pymysql.connect(**DB_CONFIG)

#teszt lekérdezés
def get_all_panels():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM cooling_panels")
            return cursor.fetchall()

#átlagos hőmérséklet panelenkét
def get_avg_panel_temperature():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT panel_id, AVG(temperature_c) AS avg_temperature
                FROM measurement_data
                GROUP BY panel_id
            """)
            return cursor.fetchall()

if __name__ == "__main__":
    ##result = get_all_panels()
    result = get_avg_panel_temperature()
    for row in result:
        print(row)


