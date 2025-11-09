import pandas as pd

class Data:
  def get_future_list(selected_year,futureYear)-> list:
    list = []
    if selected_year > futureYear:
      for year in range(futureYear,selected_year+1):
        list+= [[year]]
    else:
      list+= [[selected_year]]
    return list

  def get_df_from_csv(path)-> pd.DataFrame:
    df = pd.read_csv(path,sep=';',encoding='latin1',header=1)
    return df

  def data_manipulation(df)-> pd.DataFrame:
    df = df.set_index(df.columns[0]).T.rename_axis("Év").rename_axis("",axis="columns").reset_index().iloc[0:,0:2] #Tábla forgatás, manupulálás.
    return df