# För att säkerställa att PostgreSQL är installerat och konfigurerat korrekt.

1. check if PostgreSQL installed

```
sudo -i -u postgres
psql --version
```

2. Installera PostgreSQL

- På en Debian-baserad distribution (som Ubuntu)

```￼
  sudo apt update
  sudo apt install postgresql postgresql-contrib

```

3. Starta PostgreSQL-tjänsten:

```
sudo systemctl start postgresql
sudo systemctl enable postgresql

```

4. Skapa en databas och användare:

- Logga in på PostgreSQL:
  ￼
  ```
  sudo -i -u postgres
  psql
  ```

5. Skapa en ny användare och databas:

```
CREATE USER user WITH PASSWORD your_password;
CREATE DATABASE dbname;
GRANT ALL PRIVILEGES ON DATABASE dbname TO user;
\q
exit
```

6. hantera databasen

- kolla existerand databasen

```
\l
```

- tabort en database

```
DROP DATABASE <database name>
```

4. Läs innehållet i en PostgreSQL-databas med psql
   Logga in på PostgreSQL
   ￼

```
psql -U your_user -d your_database -h 127.0.0.1 -W
psql -U user -d dbase -h 127.0.0.1 -W

```

Om du kör PostgreSQL lokalt och använder standardinställningarna, kan du logga in med:

```
￼
psql -U postgres
```

Välj databas
Om du inte redan har valt en databas när du loggade in, kan du välja en databas med kommandot \c.

```
\c your_database

```

Visa tabeller
För att lista alla tabeller i den valda databasen, använd kommandot \dt.

```
\dt
```

Läs innehållet i en tabell
För att läsa innehållet i en specifik tabell, använd en SELECT-fråga.

```
SELECT \* FROM your_table;
```

Med dessa steg kan du enkelt läsa innehållet i en PostgreSQL-databas med `psql`.Med dessa steg kan du enkelt läsa innehållet i en PostgreSQL-databas med `psql`.

# reinstall postgress

För att installera om PostgreSQL på en Debian-baserad distribution (som Ubuntu), kan du följa dessa steg:

Ta bort den nuvarande installationen av PostgreSQL:

￼```

sudo apt-get --purge remove postgresql postgresql-contrib

sudo apt install postgresql postgresql-contrib

````

Rensa eventuella kvarvarande paket och konfigurationsfiler:

￼```

sudo apt-get autoremovesudo
apt-get autocleansudo
sudo rm -rf /var/lib/postgresql/
sudo rm -rf /etc/postgresql/

````

Uppdatera paketlistan:

￼```

sudo apt-get update

````

Installera PostgreSQL på nytt:

￼```

sudo apt-get install postgresql postgresql-contrib
````

Starta PostgreSQL-tjänsten:

```
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

Skapa en ny användare och databas:

Logga in på PostgreSQL:

￼```

sudo -i -u postgres
psql
￼```

Skapa en ny användare och databas:
￼```

CREATE USER user WITH PASSWORD 'your_password';
CREATE DATABASE dbname;
GRANT ALL PRIVILEGES ON DATABASE dbname TO user;
\q
￼```

```

```

postgres@per-PN52:/home/per/repo/rest_loader/pytesta$ sudo -i -u postgres
postgres is not in the sudoers file.
postgres@per-PN52:/home/per/repo/rest_loader/pytesta$ psql
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory
Is the server running locally and accepting connections on that socket?

sudo mkdir -p /etc/postgresql/16/main/
