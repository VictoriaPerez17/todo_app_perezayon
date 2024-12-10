import pytest
from conftest import test_client, init_database, get_created_task, test_task_data


@pytest.mark.integration_test
def test_login_create_edit_delete(test_client, init_database):
    """
    Tests task management workflow

    - Sequence followed:
        1. Login via native login
        2. Attempt task creation
        3. Attempt task update
        4. Attempt task deletion

    Assertions are the same as the one used in unit tests for each component
    """
    response = test_client.post('/login', data={"username": 'testuser', "password": 'testpassword'})
    assert response.status_code == 302

    response = test_client.post('/newTask', data=test_task_data, follow_redirects=True)
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

    assert "Test Task" in created_task.name
    assert "This is a test task" in created_task.description

    response = test_client.get("/deleteTask", query_string={"taskToDelete":created_task.id})
    created_task = get_created_task()

    assert created_task is None

@pytest.mark.integration_test
def test_login_create_complete_logout_check(test_client, init_database):
    """
    Tests task management workflow

    - Sequence followed:
        1. Login via native login
        2. Attempt task creation
        3. Attempt marking task as completed
        4. Logout
        5. GET request to /newTask

    Assertions are the same as the one used in unit tests for each component
    """
    response = test_client.post('/login', data={"username": 'testuser', "password": 'testpassword'})
    assert response.status_code == 302

    response = test_client.post('/newTask', data=test_task_data, follow_redirects=True)
    assert response.status_code == 200
    created_task = get_created_task()

    assert "Test Task" in created_task.name
    assert "This is a test task" in created_task.description

    response = test_client.get(f"/completeTask?taskToComplete={created_task.id}")
    
    created_task = get_created_task()
    print(created_task.status)
    assert created_task.status == 2

    response = test_client.get("/logout")
    assert response.headers["Location"] == "/login"

    response = test_client.get("/newTask")
    assert response.headers["Location"] == "/login"