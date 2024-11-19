# Instalación de requerimientos

Ejecutar el comando:

'''
bash
pip3 install -r requirements.txt
'''


# Crear DB en MariaDB

Ingresar a consola de MariaDB y crear una base de datos nueva

'''
sql
create database your_db_name;
'''

# Creación de archivo .env:


DATABASE = your_db_name

HOST = your_db_host

USER = your_db_user

PASSWORD = your_db_user_password

PORT = your_mariadb_port (MariaDB usa de forma predeterminada 3306)


# Creación de tablas en DB

'''
bash
python3 .\app\db_create.py
'''

# Ejecución de proyecto

'''
bash
python3 .\app\main.py
'''