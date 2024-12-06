import pytest
from main import app
from models import CoreLogin, CoreTask
from db_create import Session, create_all, drop_all
from selenium import webdriver
from selenium.webdriver.edge.options import Options


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


@pytest.fixture(scope="function")
def browser():
    options = Options()
    options.headless = True
    driver = webdriver.Edge(options=options)
    yield driver
    driver.quit()


test_task_data = {
    'taskTitle': 'Test Task',
    'taskDescription': 'This is a test task',
    'taskTS': '2024-12-31 23:59:59',
    'priority': 2
}

def get_created_task():
    with Session() as session:
        try:
            all_tasks = session.query(CoreTask).all()
            created_task = all_tasks[0]
            return created_task
        except:
            return None
        
def get_created_user():
    with Session() as session:
        try:
            all_users = session.query(CoreLogin).all()
            created_user = all_users[0]
            return created_user
        except:
            return None
        
def create_second_test_user():
    with Session() as session:
        secont_test_user = CoreLogin(username="testuser2")
        secont_test_user.set_password("password2")
        session.add(secont_test_user)
        session.commit()