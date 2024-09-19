Ejecutar el comando: 
pip3 install -r requirements.txt

Crear DB en MariaDB 

Crear archivo .env con las siguientes variables: 
DATABASE = your_db_name
HOST = your_db_host
USER = your_db_user
PASSWORD = your_db_user_password
PORT = your_mariadb_port (MariaDB usa de forma predeterminada 3306)

Ejecutar el script: 
python3 .\app\db_create.py

Ejecutar el proyecto: 
python3 .\app\main.py