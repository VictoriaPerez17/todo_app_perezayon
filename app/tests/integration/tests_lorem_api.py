from flask import url_for
from conftest import test_client, init_database, get_created_task, test_task_data


def test_create_lorem_logged_in(test_client, init_database):
    response = test_client.post('/login', data={"username": 'testuser', "password": 'testpassword'})
    assert response.status_code == 302

    response = test_client.post(url_for('list_index'), follow_redirects=True)
    assert response.status_code == 200
    created_task = get_created_task()

    assert created_task.name is not None
    assert created_task.description is not None