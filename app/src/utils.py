from db_create import Session
from models import CoreLogin, CoreTask, TaskStatus
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import joinedload


def hash_password(password):
    return generate_password_hash(password)

def authentication(username,password):
    session = Session()
    try:
        user = session.query(CoreLogin).filter_by(username=username).first()
        if user and user.check_password(password):
            return True
        return False
    finally:
        session.close()

def get_current_user_id(username):
    session = Session()
    try:
        user = session.query(CoreLogin).filter_by(username=username).first()
        if user:
            return user.id
        return None
    finally:
        session.close()

def create_user(form):
    if "username" not in form or "password" not in form:
        raise Exception("Por favor, proporcione un usuario y una contraseña")
    
    if form["username"] == "" or form["password"] == "":
        raise Exception("Por favor, proporcione un usuario y una contraseña no vacios")

    session = Session()
    try:
        user = CoreLogin(username=form["username"])
        user.set_password(form["password"])
        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()
        raise Exception("Ocurrio un error al crear al usuario: " + str(e))
    finally:
        session.close()

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
    
def create_task(task_data,user):
    session = Session()
    try:
        task = CoreTask(
            name=task_data["taskTitle"],
            description=task_data["taskDescription"],
            limit_ts=task_data["taskTS"],
            owner_user=user,
            status=1,
            priority=task_data["priority"]
        )
        session.add(task)
        session.commit()
    except Exception as e:
        session.rollback()
        raise Exception("Ocurrio un error al crear la tarea: " + str(e))
    finally:
        session.close()

def get_tasks(user):
    session = Session()
    try:
        tasks = session.query(CoreTask).options(
            joinedload(CoreTask.task_status),
            joinedload(CoreTask.task_priority)
        ).filter(CoreTask.owner_user == user).all()
        
        task_info = {
            task.id: {
                "title": task.name,
                "description": task.description,
                "status": task.task_status.status,
                "timestamp": task.limit_ts,
                "priority": task.task_priority.priority
            }
            for task in tasks
        }

        return task_info
    finally:
        session.close()

def get_task_edit(task_id):
    session = Session()
    try:
        task = session.query(CoreTask).filter_by(id=task_id).first()
        if task:
            return {
                "id": task.id,
                "current_name": task.name,
                "current_description": task.description,
                "current_status": task.task_status.status,
                "current_ts": task.limit_ts
            }
        return None
    finally:
        session.close()

def edit_task(task_data):
    session = Session()
    try:
        task = session.query(CoreTask).filter_by(id=task_data["taskID"]).first()
        if task:
            task.name = task_data["taskTitle"]
            task.description = task_data["taskDescription"]
            task.limit_ts = task_data["taskTS"]
            task.priority = task_data["priority"]
            session.commit()
    except Exception as e:
        session.rollback()
        raise Exception("Ocurrio un error al editar la tarea: " + str(e))
    finally:
        session.close()

def update_task_status(task_id,new_task_status):
    session = Session()
    try:
        status = session.query(TaskStatus).filter_by(status=new_task_status).first()
        if status:
            task = session.query(CoreTask).filter_by(id=task_id).first()
            if task:
                task.status = status.id
                session.commit()
    except Exception as e:
        session.rollback()
        raise Exception("Ocurrio un error al actualizar el estatus de la tarea: " + str(e))
    finally:
        session.close()

def delete_task(task_id):
    session = Session()
    try:
        task = session.query(CoreTask).filter_by(id=task_id).first()
        if task:
            session.delete(task)
            session.commit()
    except Exception as e:
        session.rollback()
        raise Exception("Ocurrio un error al eliminar la tarea: " + str(e))
    finally:
        session.close()