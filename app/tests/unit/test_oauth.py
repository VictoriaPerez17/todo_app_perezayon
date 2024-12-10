from requests_oauthlib import OAuth2Session
from conftest import test_client, init_database

def test_github_login_redirect(test_client):
    """Tests if unauthenticated OAUTH users are redirected to correct URL
    
    Assertions:
        - Response status code is 302 (redirection)
        - Redirect location is correct for unauthenticated user
    """
    response = test_client.get("/oauth")
    assert response.status_code == 302
    assert response.headers["Location"] == "/oauth/github" 

def test_github_callback(test_client, init_database, monkeypatch):
    """
    Tests OAUTH flow with mock response
    
    Assertions:
        - Logged in users are redirected to home page after login
        - Correct template is rendered after correct OAUTH login
        - Username and user ID are stored correctly in session data
    """
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
