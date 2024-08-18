# Install

## Setup venv

```
python3 -m venv .venv-dream100
. .venv-dream100/bin/activate
```

## Install requirements

```
pip install -r requirements-dev.txt
```

## Create .env file

This will point to a postgres database

```
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=your_database_name
   DB_USER=your_username
   DB_PASSWORD=your_password
```
