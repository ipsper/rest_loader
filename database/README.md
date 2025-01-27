# För att säkerställa att PostgreSQL är installerat och konfigurerat korrekt.

1. check if PostgreSQL installed

```
sudo -i -u postgres
psql --version
```

2. Installera PostgreSQL

- är installerat

```
dpkg -l | grep postgresql
```

- På en Debian-baserad distribution (som Ubuntu)

```
  sudo apt update
  sudo apt install postgresql postgresql-contrib

```

3. Starta PostgreSQL-tjänsten:

```
systemctl status postgresql


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
CREATE USER "user" WITH PASSWORD 'your_password';
CREATE DATABASE dbname;
GRANT ALL PRIVILEGES ON DATABASE dbname TO "user";
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
psql -U user -d dbname -h 127.0.0.1 -W

```

Om du kör PostgreSQL lokalt och använder standardinställningarna, kan du logga in med:

```

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

Skapa en ny användare och databas:

```

CREATE USER user WITH PASSWORD 'your_password';
CREATE DATABASE dbname;
GRANT ALL PRIVILEGES ON DATABASE dbname TO user;
\q
```

```

```

postgres@per-PN52:/home/per/repo/rest_loader/pytesta$ sudo -i -u postgres
postgres is not in the sudoers file.
postgres@per-PN52:/home/per/repo/rest_loader/pytesta$ psql
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory
Is the server running locally and accepting connections on that socket?

sudo mkdir -p /etc/postgresql/16/main/

sudo mkdir -p /var/lib/postgresql/
sudo mkdir -p /etc/postgresql/

sudo mkdir -p /etc/postgresql/16/main/

sudo vi /etc/postgresql/16/main/postgresql.conf
listen_addresses = '\*'
sudo vi /etc/postgresql/16/main/pg_hba.conf

host all all 127.0.0.1/32 md5

sudo mkdir -p /var/lib/postgresql/16/main
sudo chown -R postgres:postgres /var/lib/postgresql/16/main
sudo chmod 700 /var/lib/postgresql/16/main

1. Ta bort PostgreSQL helt
   Använd följande kommando för att ta bort alla PostgreSQL-relaterade paket helt och hållet:

```

sudo apt purge postgresql* -y
```

- Kontrollera om några relaterade paket fortfarande finns med:

```
dpkg -l | grep postgresql
```

- Om några poster fortfarande visas, ta bort dem manuellt:

```
sudo apt remove --purge postgresql-client-common postgresql-common -y
```

2. Ta bort kvarvarande PostgreSQL-filer och kataloger

- Ta bort alla konfigurations- och databasfiler:

```
sudo rm -rf /var/lib/postgresql/
sudo rm -rf /var/log/postgresql/
sudo rm -rf /etc/postgresql/
sudo rm -rf ~/.psql_history
```

3. Uppdatera pakethanteraren
   Kör följande kommando för att rensa bort onödiga paket och uppdatera systemet:

```
sudo apt autoremove -y
sudo apt autoclean
```

Verifiera att PostgreSQL är helt borttaget genom att köra:

```

psql --version
```

- Om det fortfarande visas, kontrollera om någon installation är från en tredjeparts-PPA (t.ex. pgdg) genom att köra:

```

which psql
```

- Om det pekar på /usr/local/bin/psql, ta bort den manuellt:

```

sudo rm /usr/bin/psql
```

4. Installera om PostgreSQL
   Efter att du har säkerställt att PostgreSQL är borttaget, installera det på nytt:

```
sudo apt update
sudo apt install postgresql postgresql-contrib -y
```

5. Kontrollera installationen
   Starta tjänsten och kontrollera att PostgreSQL körs korrekt:

```

sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl status postgresql

```

- Logga sedan in i databasen för att bekräfta att den fungerar:

```
sudo -u postgres psql
```

- Skapa en ny användare och databas:

```
CREATE USER "user" WITH PASSWORD 'your_password';
CREATE DATABASE dbname;
GRANT ALL PRIVILEGES ON DATABASE dbname TO "user";

\q
```

# problem

## psycopg2.errors.InsufficientPrivilege: permission denied for schema public

Logga in på PostgreSQL som superuser: Logga in på PostgreSQL som superuser (vanligtvis postgres):

```
sudo -i -u postgres
psql
```

Ge användaren nödvändiga privilegier: Ge användaren user nödvändiga privilegier för att skapa tabeller i schemat public:

```

GRANT ALL PRIVILEGES ON SCHEMA public TO "user";
ALTER USER "user" WITH SUPERUSER;
```

Avsluta psql-prompten: Avsluta psql-prompten:

```￼
\q

```

Försök att initiera databasen igen: Försök att initiera databasen igen genom att köra din FastAPI-applikation.

# städa bort en databas

Lösning: Koppla bort aktiva användare och ta bort databasen
Koppla bort alla aktiva sessioner manuellt:

Kör följande SQL-fråga från en annan databas (t.ex. postgres) för att avsluta alla aktiva sessioner för databasen dbname:

````
sudo -i -u postgres
psql

```￼
- städa

```￼
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'dbname';
```￼

Ta bort databasen efter att sessionerna avslutats:

Efter att sessionerna har avslutats, kör kommandot för att ta bort databasen:
```￼
DROP DATABASE dbname;

````
