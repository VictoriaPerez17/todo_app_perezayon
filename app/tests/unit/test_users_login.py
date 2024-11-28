from conftest import test_client, init_database, get_created_task, get_created_user
from utils import hash_password
from werkzeug.security import check_password_hash


def test_create_valid_user(test_client, init_database):
    response = test_client.post("createUser",data={"username":"newUser","password":"newPass"})

    created_user = get_created_user()
    assert created_user is not None

    assert response.headers["Location"] == "/login"
    response = test_client.get("/login")
    assert "Usuario creado exitosamente" in response.text

def test_create_invalid_user(test_client, init_database):
    response = test_client.post("createUser",data={"username":"newUser","password":""})

    created_user = get_created_user()
    assert created_user.username != "newUser"

    assert response.headers["Location"] == "/login"
    response = test_client.get("/login")
    print(response.text)
    assert "no vacios" in response.text

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