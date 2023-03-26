# mealbackend

$ source pgadmin4/bin/activate
$ pgadmin4

$ sudo mkdir /var/lib/pgadmin
$ sudo mkdir /var/log/pgadmin
$ sudo chown $USER /var/lib/pgadmin
$ sudo chown $USER /var/log/pgadmin
$ python3 -m venv pgadmin4
$ source pgadmin4/bin/activate
(pgadmin4) $ pip install pgadmin4
...
(pgadmin4) $ pgadmin4

First, create an empty migration:

./manage.py makemigrations myapp --empty
Then open the file and add UnaccentExtension to operations:

from django.contrib.postgres.operations import UnaccentExtension

class Migration(migrations.Migration):

    dependencies = [
        (<snip>)
    ]

    operations = [
        UnaccentExtension()
    ]

#ALTER ROLE <user_name> SUPERUSER;

#CREATE EXTENSION IF NOT EXISTS unaccent;

    sudo -u postgres psql

    GRANT TEMP ON DATABASE databaseName TO userName;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO userName;
    GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO userName;
    GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO userName;

    CREATE DATABASE dbname;

    alter user testuser with encrypted password 'qwerty';
    grant all privileges on database recul to <db_user>;
