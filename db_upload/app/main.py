from sql.sql import Database
import pandas as pd
import time
from data.data import Data

def main():
    print("App Started.")

    # Táblázat beolvasás és manipuláció
    df_raw = Data.get_df_from_csv("data/raw_panel.csv")
    print(df_raw)

    #db = Database("mysqldb",3306,"dm","dmpass")
    db = Database("127.0.0.1",3306,"db_bead","db_pass")

    
    while db.isRdy() == 0:
          print("Waiting for database to become available...")
          time.sleep(5)

    print("Connection OK.")

if __name__ == "__main__":
    main()