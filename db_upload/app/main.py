from sql.sql import Database
import pandas as pd
import time
from data.data import Data

def main():
    print("App Started.")

    #Panelek
    # Táblázat beolvasás és manipuláció
    df = Data.get_df_from_csv("data/raw_panel.csv")
    df_header = pd.read_csv("data/raw_panel.csv",sep=';',header=0) #más a kódolos.... muszáj még1x beolvasni

    cooling_panels_rows = []

    for i in range(0, df_header.shape[1], 2):
        colname = df_header.columns[i]
        short = colname.split('[')[0].strip()

        cooling_panels_rows.append({
            "panel_id": short.split()[-1],
            "panel_name": short,
        })

    cooling_panels_df = pd.DataFrame(cooling_panels_rows)

    print(cooling_panels_df)

    tables = []
    # 2 oszloponként lépünk végig (0, 2, 4, ..., 26)
    for i in range(0, df.shape[1], 2):

        # kiválasztjuk a 2 oszlopot
        sub = df.iloc[:, i:i+2].copy()

        # új DataFrame, ahol:
        # - "index_id" az aktuális panel (pl. i//2)
        # - a 2. és 3. oszlop a kivágott adatok
        new_df = pd.DataFrame({
            "panel_id": [(i // 2) + 1] * len(sub),  # minden sorhoz ugyanaz az index
            "timestamp": sub.iloc[:, 0].values,
            "temperature_c": sub.iloc[:, 1].values
        })

        tables.append(new_df)

    df_long = pd.concat(tables, ignore_index=True)

    # Tizedesvesszők javítása, majd float konverzió
    df_long["temperature_c"] = (
        df_long["temperature_c"]
        .astype(str)                # biztosan stringgé
        .str.replace(",", ".", regex=False)  # vessző → pont
        .astype(float)              # majd float-tá konvertálás
    )



    #Adagok
    # Táblázat beolvasás és manipuláció
    portions_df = Data.get_df_from_csv("data/Adagok.csv")
    portions_df = portions_df.dropna(how='all')  # Eldobja az összes olyan sort, ahol minden cella NaN (azaz üres)
    portions_df.columns = ["dose_id", "start_date", "start_time", "end_date", "end_time", "interval_sec", "duration_min"]


    db = Database("mysqldb",3306,"db_bead","db_pass")
    #db = Database("127.0.0.1",3306,"db_bead","db_pass")

    while db.isRdy() == 0:
          print("Waiting for database to become available...")
          time.sleep(5)
    print("Connection OK.")


    if(db.tableHasData("cooling_panels")):
        print("cooling_panels Data rdy.")
    else:    
        print("cooling_panels Upload to DB.")
        db.cooling_panels_df_to_db(cooling_panels_df)
        print("cooling_panels Upload Finished.")

    if(db.tableHasData("doses")):
        print("doses Data rdy.")
    else:    
        print("portions_df Upload to DB.")
        db.portions_df_to_db(portions_df)
        print("portions_df Upload Finished.")

    
    if(db.tableHasData("measurement_data")):
        print("measurement_data Data rdy.")
    else:    
        print("measurement_data Upload to DB.")
        db.measurement_data_df_to_db(df_long)
        print("measurement_data Upload Finished.")


if __name__ == "__main__":
    main()