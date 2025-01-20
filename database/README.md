## För att säkerställa att PostgreSQL är installerat och konfigurerat korrekt, kan du använda följande steg:

## is PostgreSQL installed

´´´￼
psql --version
´´´￼

1. Installera PostgreSQL:

- På en Debian-baserad distribution (som Ubuntu):

  ´´´￼
  sudo apt update
  sudo apt install postgresql postgresql-contrib
  ´´´

2. Starta PostgreSQL-tjänsten:

```
sudo systemctl start postgresql
sudo systemctl enable postgresql

```

3. Skapa en databas och användare:

- Logga in på PostgreSQL:
  ￼
  ```
  sudo -i -u postgres
  psql
  ```

4. Skapa en ny användare och databas:

```
CREATE USER user WITH PASSWORD your_password;
CREATE DATABASE dbname;
GRANT ALL PRIVILEGES ON DATABASE dbname TO user;
\q
exit
```

5. hantera databasen

- kolla existerand databasen

```
\l
```

- tabort en database

```
DROP DATABASE <database name>
```
