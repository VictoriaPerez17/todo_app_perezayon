import pytest
from main import app
from models import CoreLogin, CoreTask
from db_create import Session, init_db, drop_all
from selenium import webdriver
from selenium.webdriver.edge.options import Options


@pytest.fixture(scope='function')
def test_client():
    """Provides the client used to make requests in testing functions, creates a DB instance and drops it"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'tests'
    init_db()
    with app.test_client() as client:
        yield client
    drop_all()


@pytest.fixture(scope='function')
def init_database():
    """Creates the DB instance used in testing functions"""
    session = Session()
    test_user = CoreLogin(username='testuser')
    test_user.set_password('testpassword')
    session.add(test_user)
    session.commit()
    yield session
    session.close()


@pytest.fixture(scope="function")
def edge_browser():
    """Creates Microsoft Edge webdriver used in E2E testing"""
    options = Options()
    options.headless = True
    driver = webdriver.Edge(options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def chrome_browser():
    """Creates Chrome webdriver used in E2E testing"""
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


test_task_data = {
    'taskTitle': 'Test Task',
    'taskDescription': 'This is a test task',
    'taskTS': '2024-12-31 23:59:59',
    'priority': 2
}

def get_created_task():
    """Returns data for latest CoreTask table entry"""
    with Session() as session:
        try:
            all_tasks = session.query(CoreTask).all()
            created_task = all_tasks[0]
            return created_task
        except:
            return None
        
def get_created_user():
    """Returns data for latest CoreLogin table entry"""
    with Session() as session:
        try:
            all_users = session.query(CoreLogin).all()
            created_user = all_users[0]
            return created_user
        except:
            return None
        
def create_second_test_user():
    """Creates a second test entry in CoreLogin table"""
    with Session() as session:
        secont_test_user = CoreLogin(username="testuser2")
        secont_test_user.set_password("password2")
        session.add(secont_test_user)
        session.commit()