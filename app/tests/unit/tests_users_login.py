from conftest import test_client, init_database, get_created_task
from utils import hash_password
from werkzeug.security import check_password_hash


def test_login_valid_user(test_client, init_database):
    response = test_client.post('/login',data={"username": 'testuser', "password": 'testpassword'})
    
    assert response.headers["Location"] == "/"

def test_login_non_existing_user(test_client, init_database):
    response = test_client.post('/login',data={"username": 'testuser100', "password": 'testpassword?'})
    
    assert response.headers["Location"] == "/login"

    response = test_client.get('/login')
    assert "Error al iniciar sesion" in response.text

def test_password_hash():
    password = "hashedpassword"
    hashed_pw = hash_password(password)

    assert password != hash_password
    assert check_password_hash(hashed_pw, password)