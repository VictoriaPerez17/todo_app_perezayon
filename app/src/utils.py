import markdown
import bleach
import requests
import os
import json
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import joinedload
from dotenv import load_dotenv
from flask_dance.contrib.github import make_github_blueprint
from db_create import Session
from models import CoreLogin, CoreTask, TaskStatus


allowed_tags = ["p","strong","em","u","h1","h2","h3","h4","h5","h6","ul","ol","li","img"]
allowed_attrs = ["src","alt"]

def get_ouath_data():
    blueprint = None
    load_dotenv()
    try:
        blueprint = make_github_blueprint(client_id=os.getenv("CLIENT_ID"), client_secret=os.getenv("CLIENT_SECRET"))
        return blueprint
    except Exception as e:
        raise e

def hash_password(password):
    return generate_password_hash(password)

def add_github_user(username, github_id):
    session = Session()
    try:
        new_user = CoreLogin(username=username, github_id=github_id)
        session.add(new_user)
        session.commit()
        return new_user.id
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


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

def get_current_user_id_by_github_id(github_id):
    session = Session()
    try:
        user = session.query(CoreLogin).filter_by(github_id=github_id).first()
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
    clean_title = bleach.clean(task_data["taskTitle"], tags=allowed_tags, attributes=allowed_attrs)
    clean_desc = bleach.clean(task_data["taskDescription"],tags=allowed_tags, attributes=allowed_attrs)
    clean_title = markdown.markdown(clean_title, extensions=["extra"])
    clean_desc = markdown.markdown(clean_desc, extensions=["extra"])
    try:
        task = CoreTask(
            name=clean_title,
            description=  clean_desc,
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

def lorem_task(user):
    API_KEY = ""
    try:
        load_dotenv()
        API_KEY = os.getenv("API_KEY")

        if API_KEY == "":
            raise Exception("API Key for Lorem tasks was empty, please provide en API Key")
    except Exception as e:
        raise Exception("Ocurrio un error al obtener el API Key para tareas Lorem: " + str(e))

    api_url = "https://api.api-ninjas.com/v1/loremipsum?max_length=25&paragraphs=1&start_with_lorem_ipsum=false"
    task_title = ""
    task_description = ""
    try:
        title_response = requests.get(api_url, headers={"X-Api-Key":API_KEY})
        description_response = requests.get(api_url, headers={"X-Api-Key":API_KEY})

        if title_response.status_code == requests.codes.ok and description_response.status_code == requests.codes.ok:
            title_json = json.loads(bleach.clean(title_response.text))
            description_json = json.loads(bleach.clean(description_response.text))
            task_title = title_json["text"]
            task_description = description_json["text"]
        else:
            raise Exception(f"Lorem API did not return a success status code: {str(title_response.status_code)} | {str(description_response.status_code)}")
    except Exception as e:
        raise Exception("Ocurrio un error al generar la tarea Lorem" + str(e))
    
    session = Session()
    try:
        task = CoreTask(
            name=task_title,
            description=task_description,
            limit_ts="2024-12-25 09:00",
            owner_user=user,
            status=1,
            priority=2
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
        ).order_by(CoreTask.priority.desc()).filter(CoreTask.owner_user == user).all()
        
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

def get_task_edit(task_id, username):
    session = Session()
    try:
        task = session.query(CoreTask).filter_by(id=task_id).first()

        if task is not None:
            if task.owner_user == get_current_user_id(username):
                return {
                    "id": task.id,
                    "current_name": task.name,
                    "current_description": task.description,
                    "current_status": task.task_status.status,
                    "current_ts": task.limit_ts
                }
            else:
                raise Exception("User is not allowed to edit specified task")
        else:
            raise Exception("Task to update was not found")
    finally:
        session.close()

def edit_task(task_data, username):
    session = Session()
    try:
        task = session.query(CoreTask).filter_by(id=task_data["taskID"]).first()    
        if not task.owner_user == get_current_user_id(username):
            raise Exception("User is not allowed to edit specified task")
        
        clean_title = bleach.clean(task_data["taskTitle"], tags=allowed_tags, attributes=allowed_attrs)
        clean_desc = bleach.clean(task_data["taskDescription"],tags=allowed_tags, attributes=allowed_attrs)
        clean_title = markdown.markdown(clean_title, extensions=["extra"])
        clean_desc = markdown.markdown(clean_desc, extensions=["extra"])
        if task:
            task.name = clean_title
            task.description = clean_desc
            task.limit_ts = task_data["taskTS"]
            task.priority = task_data["priority"]
            session.commit()
    except Exception as e:
        session.rollback()
        raise Exception("Ocurrio un error al editar la tarea: " + str(e))
    finally:
        session.close()

def update_task_status(task_id,new_task_status, username):
    session = Session()
    try:
        status = session.query(TaskStatus).filter_by(status=new_task_status).first()
        if status:
            task = session.query(CoreTask).filter_by(id=task_id).first()
        if task is not None:
            if task.owner_user == get_current_user_id(username):
                task.status = status.id
                session.commit()
            else:
                raise Exception("User is not allowed to edit specified task")
        else:
            raise Exception("Task to update was not found")
    except Exception as e:
        session.rollback()
        raise Exception("Ocurrio un error al actualizar el estatus de la tarea: " + str(e))
    finally:
        session.close()

def delete_task(task_id, username):
    session = Session()
    try:
        task = session.query(CoreTask).filter_by(id=task_id).first()
        if task is not None:
            if task.owner_user == get_current_user_id(username):
                session.delete(task)
                session.commit()
            else:
                raise Exception("User is not allowed to delete specified task")
        else:
            raise Exception("Task to delete was not found")
    except Exception as e:
        session.rollback()
        raise Exception("Ocurrio un error al eliminar la tarea: " + str(e))
    finally:
        session.close()