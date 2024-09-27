import pytest
from flask import url_for
from src.models import CoreTask, CoreLogin
from src.db_create import Session
from src.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_create_task_valid_input(client):
    user = CoreLogin(username="testuser")
    user.set_password("123456789")
    session = Session()
    session.add(user)
    session.commit()
    client.post(url_for("/login"),data={"username":"testuser","password":"123456789"})

    response = client.post(url_for("/newTask"),data={"taskTitle":"Test task",
                                                     "taskDescription":"This task is a test",
                                                     "taskTS":"2024-09-07 09:00",
                                                     "priority":3
                                                     })
    assert response.status_code == 200 #OK response code
    task = CoreTask.query.first()
    assert task is not None
    assert task.name == "Test task"
    assert task.priority == 3
    assert task.owner_user == user.id