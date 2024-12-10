from conftest import test_client, init_database, get_created_task


def test_create_lorem_logged_in(test_client, init_database):
    """
    Tries to create a Lorem task
    
    Assertions:
        - Task name and description are not None after attempt
    """
    response = test_client.post('/login', data={"username": 'testuser', "password": 'testpassword'})
    assert response.status_code == 302

    response = test_client.post("/taskList", follow_redirects=True)
    assert response.status_code == 200
    created_task = get_created_task()

    assert created_task.name is not None
    assert created_task.description is not None