# TO-DO APP

This is a simple To-Do list web app, developed with Flask, testing made mainly with Pytest

# Requirements installation

Run command for PIP requirements:

```bash
pip3 install -r requirements.txt
```

Run commands to install PostgreSQL and create a DB
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql.service
sudo systemctl enable postgresql.service
sudo -i -u postgres
createdb your_db_name
psql
ALTER USER postgres WITH ENCRYPTED PASSWORD 'your_db_password';
```

Run commands to install Chrome Driver (used in E2E testing):
```bash
mkdir ChromeDriver
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f
wget https://chromedriver.storage.googleapis.com/92.0.4515.107/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
chromedriver --url-base=/wd/hub
```

# Create DB in MariaDB

Enter MariaDB console and create a new database

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
python3 .\app\db_create.py
```

# Run project

```bash
python3 .\app\main.py
```