from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, TaskStatus, TaskPriority
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE")
HOST = os.getenv("HOST")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")

DATABASE_URL = f"mariadb+mariadbconnector://{USER}:{PASSWORD}@{HOST}/{DATABASE}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
    print("DB y tablas creadas")
    seed_task_status()
    seed_task_priority()

def seed_task_status():
    session = Session()
    statuses = ["Pendiente", "Terminada", "Cancelada"]

    for status in statuses:
        existing_status = session.query(TaskStatus).filter_by(status=status).first()
        if not existing_status:
            new_status = TaskStatus(status=status)
            session.add(new_status)

    try:
        session.commit()
        print("Estados insertados correctamente")
    except Exception as e:
        session.rollback()
        print(f"Error al insertar los estados: {str(e)}")
    finally:
        session.close()

def seed_task_priority():
    session = Session()
    priorities = ["Baja", "Media", "Alta"]

    for priority in priorities:
        existing_priority = session.query(TaskPriority).filter_by(priority=priority).first()
        if not existing_priority:
            new_priority = TaskPriority(priority=priority)
            session.add(new_priority)

    try:
        session.commit()
        print("Prioridades insertadas correctamente")
    except Exception as e:
        session.rollback()
        print(f"Error al insertar las prioridades: {str(e)}")
    finally:
        session.close()


def create_all():
    init_db()

def drop_all():
    Base.metadata.drop_all(bind=engine)

if __name__ == "__main__":
    init_db()