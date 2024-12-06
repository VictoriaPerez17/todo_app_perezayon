from requests_oauthlib import OAuth2Session
from conftest import test_client, init_database

def test_github_login_redirect(test_client):
    response = test_client.get("/oauth")
    assert response.status_code == 302
    assert response.headers["Location"] == "/oauth/github" 

def test_github_callback(test_client, init_database, monkeypatch):
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

        response = test_client.get("/")
        assert "Ver tareas" in response.text
        
        with test_client.session_transaction() as sess:
            assert sess["username"] == "fakeuser"
            assert sess["user_id"] is not None
