from sql.sql import Database
import pandas as pd
import time
from data.data import Data

def main():
    print("App Started.")

    # Táblázat beolvasás és manipuláció
    df = Data.get_df_from_csv("data/raw_panel.csv")

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

    print(df_long.iloc[471549]["temperature_c"])
    

    #db = Database("mysqldb",3306,"dm","dmpass")
    db = Database("127.0.0.1",3306,"db_bead","db_pass")

    while db.isRdy() == 0:
          print("Waiting for database to become available...")
          time.sleep(5)
    print("Connection OK.")

    if(db.hasData()):
        print("DB Data rdy.")
    else:    
        print("Upload to DB.")
        db.df_to_db(df_long)
        print("Upload Finished.")


if __name__ == "__main__":
    main()