import pymysql

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "db_bead",
    "password": "db_pass",
    "database": "userdb",
    "cursorclass": pymysql.cursors.DictCursor
}


def insert_dose_and_measurements():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Tranzakció kezdése
        conn.begin()

        #Új dózis beszúrása
        insert_dose = """
        INSERT INTO doses (dose_id, duration_min, start_date, start_time, end_date, end_time, interval_sec)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        dose_data = (9999, 45, '2025-11-13', '14:00:00', '2025-11-13', '14:45:00', 60)
        cursor.execute(insert_dose, dose_data)

        # Hozzátartozó mérési adat beszúrása
        insert_measurement = """
        INSERT INTO measurement_data (panel_id, temperature_c, timestamp)
        VALUES (%s, %s, %s)
        """
        measurement_rows = [
            (1, 25.6, '2025-11-13 14:01:00'),
            (1, 26.2, '2025-11-13 14:02:00'),
            (2, 24.9, '2025-11-13 14:01:30')
        ]

        for row in measurement_rows:
            cursor.execute(insert_measurement, row)

        # Tranzakció megerősítése
        conn.commit()
        print("A tranzakció sikeres!")

    except pymysql.MySQLError as e:
        conn.rollback()
        print(" A tranzakció hibás! Rolling back...")
        print("HIBA:", e)

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    insert_dose_and_measurements()