import pytest
from flask import url_for
from src.models import CoreTask, CoreLogin
from src.db_create import Session, create_all, drop_all
from src.main import app


@pytest.fixture(scope='function')
def test_client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'tests'
    create_all()
    with app.test_client() as client:
        yield client
    drop_all()


@pytest.fixture(scope='function')
def init_database():
    session = Session()
    test_user = CoreLogin(username='testuser')
    test_user.set_password('testpassword')
    session.add(test_user)
    session.commit()
    yield session
    session.close()


def test_create_task_with_valid_inputs(test_client, init_database):
    response = test_client.post('/login', data={"username": 'testuser', "password": 'testpassword'})
    assert response.status_code == 302

    form_data = {
        'taskTitle': 'Test Task',
        'taskDescription': 'This is a test task',
        'taskTS': '2024-12-31 23:59:59',
        'priority': 2
    }
    response = test_client.post(url_for('new_index'), data=form_data, follow_redirects=True)
    assert response.status_code == 200
    with Session() as session:
        all_tasks = session.query(CoreTask).all()
        created_task = all_tasks[0]

    assert "Test Task" in created_task.name
    assert "This is a test task" in created_task.description
    

def test_create_task_with_empty_inputs(test_client, init_database):
    response = test_client.post('/login', data={"username":'testuser', "password":'testpassword'})

    form_data = {
        'taskTitle': '',
        'taskDescription': '',
        'taskTS': '',
    }
    response = test_client.post(url_for('new_index'), data=form_data, follow_redirects=True)
    assert response.status_code == 200
    
    assert "No se proporciono al menos un dato requerido" in response.text


def test_create_task_with_invalid_priority(test_client, init_database):
    response = test_client.post('/login', data={"username":'testuser',"password":'testpassword'})
    form_data = {
        'taskTitle': 'Invalid priority',
        'taskDescription': 'This is a test task',
        'taskTS': '2024-12-31 23:59:59',
        'priority':100
    }
    response = test_client.post(url_for('new_index'), data=form_data,
    follow_redirects=True)
    assert response.status_code == 200

    assert "Ocurrio un error al crear la tarea" in response.text


def test_create_task_with_markup_content(test_client, init_database):    
    response = test_client.post('/login', data={"username":'testuser',"password":'testpassword'})
    form_data = {
        'taskTitle': 'Markup task',
        'taskDescription': '**Bold text**',
        'taskTS': '2024-12-31 23:59:59',
        'priority':3
    }
    response = test_client.post(url_for('new_index'), data=form_data, follow_redirects=True)
    assert response.status_code == 200
    
    with Session() as session:
        all_tasks = session.query(CoreTask).all()
        created_task = all_tasks[0]

    assert "Markup task" in created_task.name
    assert created_task.description == "<p><strong>Bold text</strong></p>"


def test_create_task_content_sanitization(test_client, init_database):
    response = test_client.post('/login', data={"username":'testuser',"password":'testpassword'})
    form_data = {
        'taskTitle': 'Sanitization task',
        'taskDescription': "<script>alert('XSS')</script>",
        'taskTS': '2024-12-31 23:59:59',
        'priority':3
    }
    response = test_client.post(url_for('new_index'), data=form_data, follow_redirects=True)
    assert response.status_code == 200
    
    with Session() as session:
        all_tasks = session.query(CoreTask).all()
        created_task = all_tasks[0]

    assert "Sanitization task" in created_task.name
    assert "<script>alert('XSS')</script>" not in created_task.description