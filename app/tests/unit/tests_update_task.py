from flask import url_for
from conftest import test_client, init_database, get_created_task, test_task_data, create_second_test_user


def test_update_task_valid_inputs(test_client, init_database):
    response = test_client.post('/login', data={"username": 'testuser', "password": 'testpassword'})
    assert response.status_code == 302

    response = test_client.post(url_for('new_index'), data=test_task_data, follow_redirects=True)
    assert response.status_code == 200
    created_task = get_created_task()

    assert "Test Task" in created_task.name
    assert "This is a test task" in created_task.description

    update_data = {
        "taskID": created_task.id,
        'taskTitle': 'Updated title',
        'taskDescription': 'Updated description',
        'taskTS': '2024-12-31 23:59:59',
        'priority': 1
    }
    response = test_client.post(f"/editTask?taskToEdit={created_task.id}", data=update_data)

    updated_task = get_created_task()

    assert "Updated title" in updated_task.name
    assert "Updated description" in updated_task.description
    assert updated_task.priority == 1

def test_markdown_sanitization_update(test_client, init_database):
    response = test_client.post('/login', data={"username": 'testuser', "password": 'testpassword'})
    assert response.status_code == 302

    response = test_client.post(url_for('new_index'), data=test_task_data, follow_redirects=True)
    assert response.status_code == 200
    created_task = get_created_task()

    assert "Test Task" in created_task.name
    assert "This is a test task" in created_task.description

    update_data = {
        "taskID": created_task.id,
        'taskTitle': '**Updated title**',
        'taskDescription': "Updated description\n<script>alert('XSS')</script>",
        'taskTS': '2024-12-31 23:59:59',
        'priority': 1
    }
    response = test_client.post(f"/editTask?taskToEdit={created_task.id}", data=update_data)

    updated_task = get_created_task()

    assert "<p><strong>Updated title</strong></p>" in updated_task.name
    assert "<script>alert('XSS')</script>" not in updated_task.description
    assert updated_task.priority == 1

def test_update_task_invalid_inputs(test_client, init_database):
    response = test_client.post('/login', data={"username": 'testuser', "password": 'testpassword'})
    assert response.status_code == 302

    response = test_client.post(url_for('new_index'), data=test_task_data, follow_redirects=True)
    assert response.status_code == 200
    created_task = get_created_task()

    assert "Test Task" in created_task.name
    assert "This is a test task" in created_task.description

    update_data = {
        "taskID": created_task.id,
        'taskTitle': '',
        'taskDescription': '',
        'taskTS': '',
        'priority': 1
    }
    response = test_client.post(f"/editTask?taskToEdit={created_task.id}", data=update_data)

    updated_task = get_created_task()

    assert "Test Task" in updated_task.name
    response = test_client.get(f"/editTask?taskToEdit={created_task.id}")
    assert "No se proporciono al menos un dato requerido" in response.text

def test_update_other_users_task(test_client, init_database):
    response = test_client.post('/login', data={"username": 'testuser', "password": 'testpassword'})
    assert response.status_code == 302

    response = test_client.post(url_for('new_index'), data=test_task_data, follow_redirects=True)
    assert response.status_code == 200
    created_task = get_created_task()

    assert "Test Task" in created_task.name
    assert "This is a test task" in created_task.description

    response = test_client.get(url_for("logout"))
    create_second_test_user()

    response = test_client.post('/login', data={"username": 'testuser2', "password": 'password2'})
    
    update_data = {
        "taskID": created_task.id,
        'taskTitle': 'Updated title',
        'taskDescription': 'Updated description',
        'taskTS': '2024-12-31 23:59:59',
        'priority': 1
    }
    response = test_client.post(f"/editTask?taskToEdit={created_task.id}", data=update_data)

    updated_task = get_created_task()

    assert "Test Task" in updated_task.name
    response = test_client.get("taskList")
    print(response.text)
    assert "User is not allowed to edit specified task" in response.text