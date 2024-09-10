from werkzeug.security import generate_password_hash,check_password_hash
import mariadb
from dotenv import load_dotenv
import os


load_dotenv()
DBParams = {
    "database":os.getenv("DATABASE"),
    "host":os.getenv("HOST"),
    "user":os.getenv("USER"),
    "password":os.getenv("PASSWORD"),
    "port":int(os.getenv("PORT"))
}

def hash_password(password):
    return generate_password_hash(password)

def verify_password(stored_password_hash,provided_password):
    return check_password_hash(stored_password_hash,provided_password)

def authentication(username,password):
    conn = None
    try:
        conn = connect_to_db()
    except Exception as e:
        raise Exception("Ocurrio un error al intentar conectar a la DB: " + str(e))

    sql_query = "select * from core_login where username = ?"
    sql_data = (username,)
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query,sql_data)
        retrieved_user = cursor.fetchone()
        
        if retrieved_user and verify_password(retrieved_user[2], password):
            return True
        return False
    except Exception as e:
        raise Exception("Ocurrio un error al intentar iniciar sesion: " + str(e))
    finally:
        cursor.close()
        conn.close()

def get_current_user_id(username):
    conn = None
    try:
        conn = connect_to_db()
    except Exception as e:
        raise Exception("Ocurrio un error al intentar conectar a la DB: " + str(e))
    
    sql_query = "select id from core_login where username = ?"
    sql_data = (username,)
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query,sql_data)
        return cursor.fetchone()[0]
    except Exception as e:
        raise Exception("Ocurrio un error al intentar iniciar sesion: " + str(e))
    finally:
        cursor.close()
        conn.close()

def create_user(form):
    required_params = ("username","password")
    for param in required_params:
        if param not in form or form[param] == "":
            raise Exception("No se proporciono al menos uno de los datos solicitados. Por favor, proporcione un usuario y una contraseña")
        
    conn = None
    try:
        conn = connect_to_db()
    except Exception as e:
        raise Exception("Ocurrio un error al intentar conectar a la DB: " + str(e))
    
    sql_query = "insert into core_login (username,password) values(?,?)"
    sql_data = (form["username"],generate_password_hash(form["password"]))
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query,sql_data)
        conn.commit()
    except Exception as e:
        raise Exception("Ocurrio un error al intentar crear el usuario: " + str(e))
    finally:
        cursor.close()
        conn.close()

def check_required_params(form):
    required_params = ("taskTitle","taskTS")
    
    for param in required_params:
        if form[param] == "":
            return False
    return True

def get_form_inputs(request):
    task_data = {}
    for param in request.form:
        task_data[param] = request.form[param] 
    return task_data

def connect_to_db():
    return mariadb.connect(**DBParams)
    
def create_task(task_data,user):
    conn = None
    try:
        conn = connect_to_db()
    except Exception as e:
        raise Exception("Ocurrio un error al intentar conectar a la DB: " + str(e))
    
    sql_query = "insert into core_task (name,description,limit_ts,owner_user) values (?,?,?,?)"
    sql_data = (task_data["taskTitle"],task_data["taskDescription"],task_data["taskTS"],user)
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query,sql_data)
        conn.commit()
    except Exception as e:
        raise Exception("Ocurrio un error al intentar insertar la tarea en la DB: " + str(e))
    finally:
        cursor.close()
        conn.close()

def get_tasks(user):
    conn = None
    try:
        conn = connect_to_db()
    except Exception as e:
        raise Exception("Ocurrio un error al intentar conectar a la DB: " + str(e))
    
    sql_query = "select task.id,task.name,task.description,status.status,task.limit_ts from core_task task join task_status status on task.status=status.id where task.owner_user = ?"
    sql_data = (user,)
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query,sql_data)
        tasks_info = {}
        for task in cursor.fetchall():
            tasks_info[task[0]] = {"title":task[1],
                                "description":task[2],
                                "status":task[3],
                                "timestamp":task[4]
                                }
        return tasks_info
    except Exception as e:
        raise Exception("Ocurrio un error al intentar obtener las tareas de la DB: " + str(e))
    finally:
        cursor.close()
        conn.close()

def get_task_edit(task_id):
    conn = None
    try:
        conn = connect_to_db()
    except Exception as e:
        raise Exception("Ocurrio un error al intentar conectar a la DB: " + str(e))
    
    sql_query = "select task.id,task.name,task.description,status.status,task.limit_ts from core_task task join task_status status on task.status=status.id where task.id = ?"
    sql_data = (task_id,)
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query,sql_data)
        returned_row = cursor.fetchone()
        task_info = {
            "id":returned_row[0],
            "current_name":returned_row[1],
            "current_description":returned_row[2],
            "current_status":returned_row[3],
            "current_ts":returned_row[4]
        }
        return task_info
    except Exception as e:
        raise Exception("Ocurrio un error al intentar obtener la tarea de la DB: " + str(e))
    finally:
        cursor.close()
        conn.close()

def edit_task(task_data):
    conn = None
    try:
        conn = connect_to_db()
    except Exception as e:
        raise Exception("Ocurrio un error al intentar conectar a la DB: " + str(e))
    
    print("connection to DB establishes")

    sql_query = "update core_task set name=?,description=?,limit_ts=? where id = ?"
    sql_data = (task_data["taskTitle"],task_data["taskDescription"],task_data["taskTS"],task_data["taskID"])
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query,sql_data)
        print("query executed")
        conn.commit()
        print("DATA WAS SENT")
    except Exception as e:
        raise Exception("Ocurrio un error al intentar insertar la tarea en la DB: " + str(e))
    finally:
        cursor.close()
        conn.close()

def update_task_status(task_id,new_task_status):
    conn = None
    try:
        conn = connect_to_db()
    except Exception as e:
        raise Exception("Ocurrio un error al intentar conectar a la DB: " + str(e))
    
    get_complete_query = "select id from task_status where status = ?"
    get_complete_data = (new_task_status,)
    complete_id = None
    cursor = conn.cursor()

    try:
        cursor.execute(get_complete_query,get_complete_data)
        complete_id = cursor.fetchone()[0]
    except Exception as e:
        cursor.close()
        conn.close()
        raise Exception("Ocurrio un error al intentar completar la tarea: " + str(e))

    sql_query = "update core_task set status=? where id=?"
    sql_data = (complete_id,task_id)
    try:
        cursor.execute(sql_query,sql_data)
        conn.commit()
    except Exception as e:
        raise Exception("Ocurrio un error al intentar completar la tarea: " + str(e))
    finally:
        cursor.close()
        conn.close()

def delete_task(task_id):
    conn = None
    try:
        conn = connect_to_db()
    except Exception as e:
        raise Exception("Ocurrio un error al intentar conectar a la DB: " + str(e))
    
    sql_query = "delete from core_task where id = ?"
    sql_data = (task_id,)
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query,sql_data)
        conn.commit()
    except Exception as e:
        raise Exception("Ocurrio un error al intentar eliminar la tarea de la DB: " + str(e))
    finally:
        cursor.close()
        conn.close()