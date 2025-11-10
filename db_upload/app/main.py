from sql.sql import Database
import pandas as pd
import time
from data.data import Data

def main():
    print("App Started.")

    # Táblázat beolvasás és manipuláció
    df = Data.get_df_from_csv("data/raw_panel.csv")


    # 2 oszloponként lépünk végig (0, 2, 4, ..., 26)
    for i in range(0, df.shape[1], 2):
        # kiválasztjuk a 2 oszlopot
        sub = df.iloc[:, i:i+2].copy()

        # új DataFrame, ahol:
        # - "index_id" az aktuális panel (pl. i//2)
        # - a 2. és 3. oszlop a kivágott adatok
        new_df = pd.DataFrame({
            "panel_index": [i//2] * len(sub),  # minden sorhoz ugyanaz az index
            "col_1": sub.iloc[:, 0].values,
            "col_2": sub.iloc[:, 1].values
        })


    print(df)

    #db = Database("mysqldb",3306,"dm","dmpass")
    db = Database("127.0.0.1",3306,"db_bead","db_pass")

    
    while db.isRdy() == 0:
          print("Waiting for database to become available...")
          time.sleep(5)

    print("Connection OK.")

if __name__ == "__main__":
    main()