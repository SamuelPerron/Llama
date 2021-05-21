# Llama, a broker mock

![tests](https://github.com/SamuelPerron/Llama/actions/workflows/tests.yml/badge.svg)

## Installation
1. **Build docker environnment**

    `docker-compose up --build`
2. **Create databases** 

    `docker-compose exec db psql -Upostgres -c "CREATE DATABASE llama;"`
    
    `docker-compose exec db psql -Upostgres -c "CREATE DATABASE test_llama;"`
3. **Run migrations**

    `docker-compose exec api flask db upgrade`

## Tests
https://pythonhosted.org/Flask-Testing/

**Running tests**

`docker-compose exec api pytest`

## Migrations
https://flask-migrate.readthedocs.io/en/latest/index.html

**Creating migrations**

`docker-compose exec api flask db migrate`

**Running migrations**

`docker-compose exec api flask db upgrade`