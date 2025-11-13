import pymysql

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "db_bead",
    "password": "db_pass",
    "database": "userdb",
    "cursorclass": pymysql.cursors.DictCursor
}

def get_connection():
    return pymysql.connect(**DB_CONFIG)

def multiple_queries():
    query = """
    SELECT
        d.dose_id,
        COUNT(m.measurement_id) AS total_measurements,
        ROUND(AVG(m.temperature_c), 2) AS avg_temperature,

        (
            SELECT MAX(md.temperature_c)
            FROM measurement_data md
            WHERE md.timestamp BETWEEN 
                CONCAT(d.start_date, ' ', d.start_time) AND 
                CONCAT(d.end_date, ' ', d.end_time)
        ) AS max_temperature,

        (
            SELECT md2.panel_id
            FROM measurement_data md2
            WHERE md2.timestamp BETWEEN 
                CONCAT(d.start_date, ' ', d.start_time) AND 
                CONCAT(d.end_date, ' ', d.end_time)
            ORDER BY md2.temperature_c DESC
            LIMIT 1
        ) AS panel_with_max_temperature,

        (
            SELECT md3.timestamp
            FROM measurement_data md3
            WHERE md3.timestamp BETWEEN 
                CONCAT(d.start_date, ' ', d.start_time) AND 
                CONCAT(d.end_date, ' ', d.end_time)
            ORDER BY md3.temperature_c DESC
            LIMIT 1
        ) AS timestamp_of_max_temperature

    FROM doses d
    JOIN measurement_data m
      ON m.timestamp BETWEEN 
         CONCAT(d.start_date, ' ', d.start_time) AND 
         CONCAT(d.end_date, ' ', d.end_time)

    GROUP BY d.dose_id
    ORDER BY d.dose_id;
    """

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                return results
    except pymysql.MySQLError as e:
        print("MySQL error:", e)
        return []


if __name__ == "__main__":
    result = multiple_queries()

    if result:
        for row in result:
            print(f"Dózis #{row['dose_id']} | Avg Temp: {row['avg_temperature']}°C | Max Temp: {row['max_temperature']}°C")
            print(f"Panel: {row['panel_with_max_temperature']}, Time: {row['timestamp_of_max_temperature']}")
    else:
        print("Nincs adat vagy hibás a lekérdezés.")
