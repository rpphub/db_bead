# DMlab Próba feladat
Gitről clone-ozás után projekt indítása dockerrel. Gyökér könyvtárból parancssor->
```
docker compose up -d

```

Elvileg requirements.txtk-ből minden konténerhez feltelepülnek a libek.
Konténerek:
- sqldb #Mysql szerver
- api_site #Egyszerű streamlit sql adatokat lekérdezi és megjeleníti(localhost:8501)
- scrapper #Két étterem napi menüjét scrappeli és sql-be teszi.
- phpmyadmin #Ez csak az sql egyszerű debuggolása miatt van.