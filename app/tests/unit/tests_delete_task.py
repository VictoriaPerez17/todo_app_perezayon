from flask import url_for
from models import CoreTask
from db_create import Session
from .conftest import test_client, init_database, get_created_task, test_task_data


def test_delete_task_without_login(test_client, init_database):
    response = test_client.post('/login', data={"username": 'testuser', "password": 'testpassword'})
    assert response.status_code == 302

    response = test_client.post(url_for('new_index'), data=test_task_data, follow_redirects=True)
    assert response.status_code == 200
    created_task = get_created_task()

    assert "Test Task" in created_task.name
    assert "This is a test task" in created_task.description

    response = test_client.get(url_for("logout"))

    response = test_client.get(url_for("delete_task_index"), query_string={"taskToDelete":created_task.id})
    created_task = get_created_task()

    assert "Test Task" in created_task.name
    assert "This is a test task" in created_task.description


def test_delete_existing_task(test_client, init_database):
    response = test_client.post('/login', data={"username": 'testuser', "password": 'testpassword'})
    assert response.status_code == 302

    response = test_client.post(url_for('new_index'), data=test_task_data, follow_redirects=True)
    assert response.status_code == 200
    created_task = get_created_task()

    assert "Test Task" in created_task.name
    assert "This is a test task" in created_task.description

    response = test_client.get(url_for("delete_task_index"), query_string={"taskToDelete":created_task.id})
    created_task = get_created_task()

    assert created_task is None


def test_delete_non_existing_task(test_client, init_database):
    response = test_client.post('/login', data={"username": 'testuser', "password": 'testpassword'})
    assert response.status_code == 302

    response = test_client.post(url_for('new_index'), data=test_task_data, follow_redirects=True)
    assert response.status_code == 200
    created_task = get_created_task()

    assert "Test Task" in created_task.name
    assert "This is a test task" in created_task.description

    response = test_client.get(url_for("delete_task_index"), query_string={"taskToDelete":5000})
    created_task = get_created_task()

    assert created_task is not None