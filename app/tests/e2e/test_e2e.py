import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from conftest import browser, test_client, init_database, get_created_task
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_login(browser, test_client, init_database):
    browser.get("http://localhost/createUser")
    time.sleep(2)

    username_field = browser.find_element(By.NAME, "username")
    password_field = browser.find_element(By.NAME, "password")

    username_field.send_keys("admin")
    password_field.send_keys("admin")
    password_field.send_keys(Keys.RETURN)
    time.sleep(2)

    assert "Usuario creado exitosamente" in browser.page_source

    username_field = browser.find_element(By.NAME, "username")
    password_field = browser.find_element(By.NAME, "password")

    username_field.send_keys("admin")
    password_field.send_keys("admin")
    password_field.send_keys(Keys.RETURN)
    time.sleep(2)

    assert "Ver tareas" in browser.page_source

    browser.get("http://localhost/newTask")
    time.sleep(2)

    assert "Crear" in browser.page_source

    title_field = browser.find_element(By.NAME, "taskTitle")
    description_field = browser.find_element(By.NAME, "taskDescription")
    timestamp_field = browser.find_element(By.NAME, "taskTS")
    title_field.send_keys("Test task")
    description_field.send_keys("This task was created during E2E testing")
    timestamp_field.send_keys("25122024")
    timestamp_field.send_keys(Keys.ARROW_RIGHT)
    timestamp_field.send_keys("12:00")
    timestamp_field.send_keys(Keys.ARROW_UP)
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.NAME, "btnSave"))
    )
    browser.find_element(By.NAME, "btnSave").click()
    created_task = get_created_task()
    time.sleep(2)

    browser.get("http://localhost")
    time.sleep(2)

    browser.get("http://localhost/taskList")
    time.sleep(2)

    browser.get("http://localhost/editTask?taskToEdit=1")
    time.sleep(2)
    assert "Guardar cambios" in browser.page_source

    title_field = browser.find_element(By.NAME, "taskTitle")
    title_field.send_keys(Keys.CONTROL + "a")
    title_field.send_keys(Keys.DELETE)
    title_field.send_keys("Edited task")
    description_field = browser.find_element(By.NAME, "taskDescription")
    description_field.send_keys(Keys.CONTROL + "a")
    description_field.send_keys(Keys.DELETE)
    description_field.send_keys("This task was edited after its creation")
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.NAME, "btnSave"))
    )
    browser.find_element(By.NAME, "btnSave").click()
    time.sleep(2)

    assert "Tarea editada correctamente" in browser.page_source

    browser.get("http://localhost/completeTask?taskToComplete=1")
    time.sleep(2)

    browser.get("http://localhost/completeTask?taskToDelete=1")
    time.sleep(2)

    browser.get("http://localhost")
    time.sleep(2)

    browser.get("http://localhost/logout")
    time.sleep(2)

    assert "Iniciar sesion" in browser.page_source