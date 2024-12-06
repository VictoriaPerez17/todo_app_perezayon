# Instalación de requerimientos

Ejecutar el comando:

```bash
pip3 install -r requirements.txt
```


# Crear DB en MariaDB

Ingresar a consola de MariaDB y crear una base de datos nueva

```sql
create database your_db_name;
```

# Creación de archivo .env

#Database Parameters


DATABASE=your_db_name

HOST=your_db_host

USER=your_db_user

PASSWORD=your_db_user_password

PORT=your_mariadb_port (MariaDB usa de forma predeterminada 3306)

#OAUTH Parameters

CLIENT_ID=your_github_oauth_client_id

CLIENT_SECRET=your_github_oauth_client_secret

OAUTHLIB_INSECURE_TRANSPORT=1 (this allows to run app on HTTP)

#LOREM API KEY

API_KEY=your_lorem_api_key

#GITHUB TEST ACCOUNT

GH_LOGIN=VictoriaPerez17

GH_PASSWORD=capulinA1

# Creación de tablas en DB

```bash
python3 .\app\db_create.py
```

# Ejecución de proyecto

```bash
python3 .\app\main.py
```