import pytest
from requests_oauthlib import OAuth2Session
from conftest import test_client, init_database, get_created_task, test_task_data


@pytest.mark.integration_test
def test_oauth_task_flow(test_client, init_database, monkeypatch):
    def fake_github_get(*args, **kwargs):
        class FakeResponse:
            ok = True

            @staticmethod
            def json():
                return {"login": "fakeuser", "id": "12345"}
        
        return FakeResponse()
    
    with test_client.application.app_context():
        monkeypatch.setattr(OAuth2Session, "get", fake_github_get)
    
        with test_client.session_transaction() as sess:
            sess["github_oauth_token"] = {"access_token": "fake_token"}
        
        response = test_client.get("/oauth")
        assert response.status_code == 302
        assert response.headers["Location"] == "/"

        response = test_client.post('/newTask', data=test_task_data, follow_redirects=True)
        assert response.status_code == 200
        created_task = get_created_task()

        assert "Test Task" in created_task.name
        assert "This is a test task" in created_task.description

        update_data = {
            "taskID": created_task.id,
            'taskTitle': 'Updated title',
            'taskDescription': 'Updated description',
            'taskTS': '2024-12-31 23:59:59',
            'priority': 1
        }
        response = test_client.post(f"/editTask?taskToEdit={created_task.id}", data=update_data)

        updated_task = get_created_task()

        assert "Updated title" in updated_task.name
        assert "Updated description" in updated_task.description
        assert updated_task.priority == 1

        assert "Test Task" in created_task.name
        assert "This is a test task" in created_task.description

        response = test_client.get("/deleteTask", query_string={"taskToDelete":created_task.id})
        created_task = get_created_task()

        assert created_task is None


@pytest.mark.integration_test
def test_oauth_session_flow(test_client, init_database, monkeypatch):
    def fake_github_get(*args, **kwargs):
        class FakeResponse:
            ok = True

            @staticmethod
            def json():
                return {"login": "fakeuser", "id": "12345"}
        
        return FakeResponse()
    
    with test_client.application.app_context():
        monkeypatch.setattr(OAuth2Session, "get", fake_github_get)
    
        with test_client.session_transaction() as sess:
            sess["github_oauth_token"] = {"access_token": "fake_token"}
        
        response = test_client.get("/oauth")
        assert response.status_code == 302
        assert response.headers["Location"] == "/"

        response = test_client.get('/newTask')
        assert response.status_code == 200
        assert "New Task" in response.text

        response = test_client.get('/logout')

        response = test_client.post('/newTask', data=test_task_data, follow_redirects=True)
        assert response.status_code == 200
        created_task = get_created_task()

        assert created_task is None