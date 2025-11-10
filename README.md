# DB beadandó
Gitről clone-ozás után projekt indítása dockerrel. Gyökér könyvtárból parancssor->
```
docker compose up -d

```

Elvileg requirements.txtk-ből minden konténerhez feltelepülnek a libek.
Konténerek:
- sqldb #Mysql szerver
- phpmyadmin #Ez csak az sql egyszerű debuggolása miatt van.