# TO-DO APP

This is a simple To-Do list web app, developed with Flask, testing made mainly with Pytest

# Requirements installation

Run command:

```bash
pip3 install -r requirements.txt
```

# Create DB in MariaDB

Enter MariaDB console and create a new database

```sql
create database your_db_name;
```

# .env file creation

#Database Parameters


DATABASE=your_db_name

HOST=your_db_host

USER=your_db_user

PASSWORD=your_db_user_password

PORT=your_mariadb_port (MariaDB uses 3306 by default)

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
python3 .\app\db_create.py
```

# Run project

```bash
python3 .\app\main.py
```