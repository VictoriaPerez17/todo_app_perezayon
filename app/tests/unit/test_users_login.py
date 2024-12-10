from conftest import test_client, init_database, get_created_task, get_created_user
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


def test_create_valid_user(test_client, init_database):
    """
    Tries to create a user with valid inputs
    
    Assertions:
        - Created user is not None after creation attempt
        - User is redirected to login screen after correct creation
        - Success flash message displayed on screen
    """
    response = test_client.post("createUser",data={"username":"newUser","password":"newPass"})

    created_user = get_created_user()
    assert created_user is not None

    assert response.headers["Location"] == "/login"
    response = test_client.get("/login")
    assert "Usuario creado exitosamente" in response.text

def test_create_invalid_user(test_client, init_database):
    """
    Tries to create a user with invalid inputs
    
    Assertions:
        - User with specified username is not created
        - User is redirected to login screen after correct creation
        - Error flash message displayed on screen
    """
    response = test_client.post("createUser",data={"username":"newUser","password":""})

    created_user = get_created_user()
    assert created_user.username != "newUser"

    assert response.headers["Location"] == "/login"
    response = test_client.get("/login")
    print(response.text)
    assert "no vacios" in response.text

def test_login_valid_user(test_client, init_database):
    """
    Tries to log in with a valid user, using native login
    
    Assertions:
        - User is redirected to home page after login attempt
    """
    response = test_client.post('/login',data={"username": 'testuser', "password": 'testpassword'})
    
    assert response.headers["Location"] == "/"

def test_login_non_existing_user(test_client, init_database):
    """
    Tries to log in with a non-existing user, using native login
    
    Assertions:
        - User is redirected to login screen after login attempt
        - Error flash message displayed on screen
    """
    response = test_client.post('/login',data={"username": 'testuser100', "password": 'testpassword?'})
    
    assert response.headers["Location"] == "/login"

    response = test_client.get('/login')
    assert "Error al iniciar sesion" in response.text

def test_password_hash():
    """
    Tests password hashing process
    
    Assertions:
        - Input password is not the same as its hash
        - Input password hash is the same as its hash
    """
    password = "hashedpassword"
    hashed_pw = generate_password_hash(password)

    assert password != hashed_pw
    assert check_password_hash(hashed_pw, password)