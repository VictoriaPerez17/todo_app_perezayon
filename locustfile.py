from locust import HttpUser, between, task
from app.src.models import CoreLogin
from app.src.db_create import Session
from app.tests.conftest import test_task_data, get_created_task
from sqlalchemy.orm.exc import NoResultFound

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    def on_start(self):
        self.init_database()

    def init_database(self):
        session = Session()
        try:
            test_user = session.query(CoreLogin).filter_by(username="testuser").one()
        except NoResultFound:
            test_user = CoreLogin(username="testuser")
            test_user.set_password("testpassword")
            session.add(test_user)
            session.commit()
        finally:
            session.close()
    
    @task
    def index(self):
        self.client.get("/")

    @task
    def taskCreation(self):
        self.client.post("/login", {
            "username": "testuser",
            "password": "testpassword"
        })
        self.client.post("/newTask", data=test_task_data)
        created_task = get_created_task()
        self.client.get(f"/deleteTask?taskToDelete={created_task.id}")