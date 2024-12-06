import pytest
import time
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from conftest import chrome_browser, test_client, init_database, get_created_task
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.slow_integration_test
def test_create_delete_task(chrome_browser, test_client, init_database):
    chrome_browser.get("http://localhost/createUser")
    time.sleep(2)

    username_field = chrome_browser.find_element(By.NAME, "username")
    password_field = chrome_browser.find_element(By.NAME, "password")

    username_field.send_keys("admin")
    password_field.send_keys("admin")
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

    assert "Usuario creado exitosamente" in chrome_browser.page_source

    username_field = chrome_browser.find_element(By.NAME, "username")
    password_field = chrome_browser.find_element(By.NAME, "password")

    username_field.send_keys("admin")
    password_field.send_keys("admin")
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

    assert "Ver tareas" in chrome_browser.page_source

    chrome_browser.get("http://localhost/newTask")
    time.sleep(5)

    assert "Crear" in chrome_browser.page_source

    title_field = chrome_browser.find_element(By.NAME, "taskTitle")
    description_field = chrome_browser.find_element(By.NAME, "taskDescription")
    timestamp_field = chrome_browser.find_element(By.NAME, "taskTS")
    title_field.send_keys("Test task")
    description_field.send_keys("This task was created during E2E testing")
    timestamp_field.send_keys("25122024")
    timestamp_field.send_keys(Keys.ARROW_RIGHT)
    timestamp_field.send_keys("12:00")
    timestamp_field.send_keys(Keys.ARROW_UP)
    WebDriverWait(chrome_browser, 10).until(
        EC.element_to_be_clickable((By.NAME, "btnSave"))
    )
    chrome_browser.find_element(By.NAME, "btnSave").click()
    created_task = get_created_task()
    time.sleep(5)

    chrome_browser.get("http://localhost/taskList")
    time.sleep(5)

    chrome_browser.get(f"http://localhost/deleteTask?taskToDelete={created_task.id}")
    time.sleep(5)

    chrome_browser.get("http://localhost")
    time.sleep(5)

    chrome_browser.get("http://localhost/logout")
    time.sleep(5)

    assert "Iniciar sesión" in chrome_browser.page_source


@pytest.mark.slow_integration_test
def test_create_task(chrome_browser, test_client, init_database):
    load_dotenv()
    login = os.getenv("GH_LOGIN")
    password = os.getenv("GH_PASSWORD")

    chrome_browser.get("http://localhost/oauth")

    username_field = chrome_browser.find_element(By.NAME, "login")
    password_field = chrome_browser.find_element(By.NAME, "password")

    username_field.send_keys(login)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

    chrome_browser.get("http://localhost/oauth")
    time.sleep(5)
    assert "Ver tareas" in chrome_browser.page_source

    chrome_browser.get("http://localhost/newTask")
    time.sleep(5)

    assert "Crear" in chrome_browser.page_source

    title_field = chrome_browser.find_element(By.NAME, "taskTitle")
    description_field = chrome_browser.find_element(By.NAME, "taskDescription")
    timestamp_field = chrome_browser.find_element(By.NAME, "taskTS")
    title_field.send_keys("Test task")
    description_field.send_keys("This task was created during E2E testing")
    timestamp_field.send_keys("25122024")
    timestamp_field.send_keys(Keys.ARROW_RIGHT)
    timestamp_field.send_keys("12:00")
    timestamp_field.send_keys(Keys.ARROW_UP)
    WebDriverWait(chrome_browser, 10).until(
        EC.element_to_be_clickable((By.NAME, "btnSave"))
    )
    chrome_browser.find_element(By.NAME, "btnSave").click()
    created_task = get_created_task()
    time.sleep(5)

    chrome_browser.get("http://localhost/taskList")
    time.sleep(5)

    chrome_browser.get(f"http://localhost/editTask?taskToEdit={created_task.id}")
    time.sleep(5)
    assert "Guardar cambios" in chrome_browser.page_source

    title_field = chrome_browser.find_element(By.NAME, "taskTitle")
    title_field.send_keys(Keys.CONTROL + "a")
    title_field.send_keys(Keys.DELETE)
    title_field.send_keys("Edited task")
    description_field = chrome_browser.find_element(By.NAME, "taskDescription")
    description_field.send_keys(Keys.CONTROL + "a")
    description_field.send_keys(Keys.DELETE)
    description_field.send_keys("This task was edited after its creation")
    WebDriverWait(chrome_browser, 10).until(
        EC.element_to_be_clickable((By.NAME, "btnSave"))
    )
    chrome_browser.find_element(By.NAME, "btnSave").click()
    time.sleep(5)

    assert "Tarea editada correctamente" in chrome_browser.page_source

    chrome_browser.get("http://localhost/taskList")
    time.sleep(5)

    chrome_browser.get(f"http://localhost/completeTask?taskToComplete={created_task.id}")
    time.sleep(5)

    assert "Tarea completada correctamente" in chrome_browser.page_source

    chrome_browser.get("http://localhost/logout")
    time.sleep(5)

    assert "Iniciar sesión" in chrome_browser.page_source