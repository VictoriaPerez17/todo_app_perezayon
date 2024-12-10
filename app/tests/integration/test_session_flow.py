import pytest
from conftest import test_client, init_database, get_created_task, test_task_data, create_second_test_user

@pytest.mark.integration_test
def test_check_login_check_logout_check(test_client, init_database):
    """
    Tests session management workflow

    - Sequence followed:
        1. Attempt task creation
        2. Login via native login
        3. GET request to /newTask
        4. Logout
        5. Attempt task creation

    Assertions are the same as the one used in unit tests for each component
    """
    response = test_client.post('/newTask', data=test_task_data, follow_redirects=True)
    assert response.status_code == 200
    created_task = get_created_task()

    assert created_task is None

    response = test_client.post('/login', data={"username": 'testuser', "password": 'testpassword'})
    assert response.status_code == 302

    response = test_client.get('/newTask')
    assert response.status_code == 200
    assert "New Task" in response.text

    response = test_client.get('/logout')

    response = test_client.post('/newTask', data=test_task_data, follow_redirects=True)
    assert response.status_code == 200
    created_task = get_created_task()

    assert created_task is None

@pytest.mark.integration_test
def test_different_users_task_listing(test_client, init_database):
    """
    Tests session management workflow

    - Sequence followed:
        1. Create second test user
        2. Login as first test user
        3. Attempt task creation
        4. Logout
        5. Login as second test user
        6. Attempt task creation
        7. GET request to /taskList

    Assertions are the same as the one used in unit tests for each component
    """
    create_second_test_user()

    response = test_client.post('/login', data={"username": 'testuser', "password": 'testpassword'})
    assert response.status_code == 302

    response = test_client.post('/newTask', data=test_task_data, follow_redirects=True)
    assert response.status_code == 200
    created_task = get_created_task()

    response = test_client.get("/logout")

    response = test_client.post('/login', data={"username": 'testuser2', "password": 'password2'})
    assert response.status_code == 302

    form_data = {
        'taskTitle': 'Markup task',
        'taskDescription': '**Bold text**',
        'taskTS': '2024-12-31 23:59:59',
        'priority':3
    }

    response = test_client.post('/newTask', data=form_data, follow_redirects=True)
    assert response.status_code == 200
    
    response = test_client.get("/taskList")
    
    assert "Test Task" not in response.text
    assert  "This is a test task" not in response.text
    assert "Markup task" in response.text
    assert "Bold text" in response.text