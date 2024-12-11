# TO-DO APP

This is a simple To-Do list web app, developed with Flask, testing made mainly with Pytest
Below is given the process to locally test and run the project.
A comprehensive step-by-step deployment guide may be watched at https://youtu.be/KWIIPKbdxD0?feature=shared

## Database setup

Run commands to install PostgreSQL and create a DB
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql.service
sudo systemctl enable postgresql.service
sudo -i -u postgres
createdb your_db_user
psql
CREATE USER your_db_user PASSWORD 'your_db_password';
ALTER USER your_db_user createdb;
sudo -i -u your_db_user
psql
create database your_db;
```

## Repo cloning and requirements installation

```bash
git clone https://github.com/VictoriaPerez17/todo_app_perezayon.git
cd todo_app_perezayon/
python3 -m venv ./venv
sudo chmod -R a+rwx ./venv
pip3 install -r requirements.txt
```

# .env file creation

#Database Parameters


DATABASE=your_db_name

HOST=your_db_host

USER=your_db_user

PASSWORD=your_db_user_password

PORT=your_postgresql_port (PosgreSQL uses 5432 by default)

#OAUTH Parameters

CLIENT_ID=your_github_oauth_client_id

CLIENT_SECRET=your_github_oauth_client_secret

OAUTHLIB_INSECURE_TRANSPORT=1 (this allows to run app on HTTP)

#LOREM API KEY

API_KEY=your_lorem_api_key

#GITHUB TEST ACCOUNT

GH_LOGIN=YourGithubUser

GH_PASSWORD=YourGithubPassword

# DB tables creation

```bash
source ./venv/bin/activate
python3 ./app/src/db_create.py
```

# Test project

```bash
source ./venv/bin/activate
pytest
```

# Run project

```bash
source ./venv/bin/activate
python3 ./app/main.py
```