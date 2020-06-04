# Vin Lookup

This is a site I quickly put together to find out what Kia Telluride's were being produced and what dealers they are going to.

This is being hosted on [Heroku](http://telluride-lookup.herokuapp.com/).

For more info on Tellurides, I recommend [this forum](https://tellurideforum.org/)

## Running locally
Database is Postgres

### Set database url
> export DATABASE_URL=postgresql://localhost/telly

### Setup the postgres database:

> python manage.py db init

> python manage.py db migrate

> python manage.py db upgrade

### Import the data:

> pg_restore --verbose --clean --no-acl --no-owner -h localhost -d telly latest.dump

### Run it locally:
> python run.py runserver

