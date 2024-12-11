import pytest
import time
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from conftest import edge_browser, test_client, init_database, get_created_task
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.slow_integration_test
def test_create_delete_task(edge_browser, test_client, init_database):
    """
    Tests task management workflow with Edge WebDriver

    - Sequence followed:
        1. Attempt native user creation
        2. Attempt task creation
        3. Attempt task deletion
        4. Logout

    Assertions are the same as the one used in unit tests for each component
    """
    edge_browser.get("http://localhost:5000/createUser")
    time.sleep(2)

    username_field = edge_browser.find_element(By.NAME, "username")
    password_field = edge_browser.find_element(By.NAME, "password")

    username_field.send_keys("admin")
    password_field.send_keys("admin")
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

    assert "Usuario creado exitosamente" in edge_browser.page_source

    username_field = edge_browser.find_element(By.NAME, "username")
    password_field = edge_browser.find_element(By.NAME, "password")

    username_field.send_keys("admin")
    password_field.send_keys("admin")
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

    assert "Ver tareas" in edge_browser.page_source

    edge_browser.get("http://localhost:5000/newTask")
    time.sleep(5)

    assert "Crear" in edge_browser.page_source

    title_field = edge_browser.find_element(By.NAME, "taskTitle")
    description_field = edge_browser.find_element(By.NAME, "taskDescription")
    timestamp_field = edge_browser.find_element(By.NAME, "taskTS")
    title_field.send_keys("Test task")
    description_field.send_keys("This task was created during E2E testing")
    timestamp_field.send_keys("25122024")
    timestamp_field.send_keys(Keys.ARROW_RIGHT)
    timestamp_field.send_keys("12:00")
    timestamp_field.send_keys(Keys.ARROW_UP)
    WebDriverWait(edge_browser, 10).until(
        EC.element_to_be_clickable((By.NAME, "btnSave"))
    )
    edge_browser.find_element(By.NAME, "btnSave").click()
    created_task = get_created_task()
    time.sleep(5)

    edge_browser.get("http://localhost:5000/taskList")
    time.sleep(5)

    edge_browser.get(f"http://localhost:5000/deleteTask?taskToDelete={created_task.id}")
    time.sleep(5)

    edge_browser.get("http://localhost:5000")
    time.sleep(5)

    edge_browser.get("http://localhost:5000/logout")
    time.sleep(5)

    assert "Iniciar sesión" in edge_browser.page_source


@pytest.mark.slow_integration_test
def test_create_task(edge_browser, test_client, init_database):
    """
    Tests task management workflow with Edge WebDriver

    - Sequence followed:
        1. Attempt native user creation
        2. Attempt task creation
        3. Attempt task deletion
        4. Logout

    Assertions are the same as the one used in unit tests for each component
    """
    load_dotenv()
    login = os.getenv("GH_LOGIN")
    password = os.getenv("GH_PASSWORD")

    edge_browser.get("http://localhost:5000/oauth")

    username_field = edge_browser.find_element(By.NAME, "login")
    password_field = edge_browser.find_element(By.NAME, "password")

    username_field.send_keys(login)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

    edge_browser.get("http://localhost:5000/oauth")
    time.sleep(5)
    assert "Ver tareas" in edge_browser.page_source

    edge_browser.get("http://localhost:5000/newTask")
    time.sleep(5)

    assert "Crear" in edge_browser.page_source

    title_field = edge_browser.find_element(By.NAME, "taskTitle")
    description_field = edge_browser.find_element(By.NAME, "taskDescription")
    timestamp_field = edge_browser.find_element(By.NAME, "taskTS")
    title_field.send_keys("Test task")
    description_field.send_keys("This task was created during E2E testing")
    timestamp_field.send_keys("25122024")
    timestamp_field.send_keys(Keys.ARROW_RIGHT)
    timestamp_field.send_keys("12:00")
    timestamp_field.send_keys(Keys.ARROW_UP)
    WebDriverWait(edge_browser, 10).until(
        EC.element_to_be_clickable((By.NAME, "btnSave"))
    )
    edge_browser.find_element(By.NAME, "btnSave").click()
    created_task = get_created_task()
    time.sleep(5)

    edge_browser.get("http://localhost:5000/taskList")
    time.sleep(5)

    edge_browser.get(f"http://localhost:5000/editTask?taskToEdit={created_task.id}")
    time.sleep(5)
    assert "Guardar cambios" in edge_browser.page_source

    title_field = edge_browser.find_element(By.NAME, "taskTitle")
    title_field.send_keys(Keys.CONTROL + "a")
    title_field.send_keys(Keys.DELETE)
    title_field.send_keys("Edited task")
    description_field = edge_browser.find_element(By.NAME, "taskDescription")
    description_field.send_keys(Keys.CONTROL + "a")
    description_field.send_keys(Keys.DELETE)
    description_field.send_keys("This task was edited after its creation")
    WebDriverWait(edge_browser, 10).until(
        EC.element_to_be_clickable((By.NAME, "btnSave"))
    )
    edge_browser.find_element(By.NAME, "btnSave").click()
    time.sleep(5)

    assert "Tarea editada correctamente" in edge_browser.page_source

    edge_browser.get("http://localhost:5000/taskList")
    time.sleep(5)

    edge_browser.get(f"http://localhost:5000/completeTask?taskToComplete={created_task.id}")
    time.sleep(5)

    assert "Tarea completada correctamente" in edge_browser.page_source

    edge_browser.get("http://localhost:5000/logout")
    time.sleep(5)

    assert "Iniciar sesión" in edge_browser.page_source