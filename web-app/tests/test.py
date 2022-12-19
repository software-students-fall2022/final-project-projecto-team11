from app import create_app
from app.db import get_translations_collection, get_users_collection, insert_sample_data
import pytest
import mongomock
import os

class Tests: # pragma: no cover
    @pytest.fixture
    def mongo_client(self):
        mock_client = mongomock.MongoClient('mongodb://localhost:27017')
        mock_translations_collection = mock_client.translator.translations
        mock_translations_collection.insert_one({
            "_id": "634f028fa11c10159ae12607",
            "user": "634f028fa11c10159ae12607",
            "translation": {
                "inputLanguage": "de",
                "inputText": "Guten tag.",
                "outputText": "Good morning.",
                "outputLanguage": "en"
            },
            "status": {
                "message": "SUCCESS",
                "update": 1666122383
            }
        })
        yield mock_client
        mock_translations_collection.drop()

    @pytest.fixture
    def app(self, mongo_client):
        app = create_app({
            "TESTING": True,
            "MONGO_CLIENT": mongo_client
        })
        return app

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def test_insert_sample_data(self, mongo_client): 
        mongo_client.translator.users.drop()
        assert get_users_collection(mongo_client).find_one({"name":"admin"}) is None

        dir_path = os.path.dirname(os.path.realpath(__file__))
        user_data_path = os.path.join(dir_path, './sample_user_data.json')
        translation_data_path = os.path.join(dir_path, './sample_translation_data.json')
        insert_sample_data(mongo_client, user_data_path, translation_data_path)

        assert get_translations_collection(mongo_client).find_one({"translation.inputLanguage":"de"}) is not None

    def test_get_translations_collection(self, mongo_client):
        translations_collection = get_translations_collection(mongo_client)
        input_languages = ["de", "es", "fr", "ja"]
        for input_language in input_languages:
            assert get_translations_collection(mongo_client).find_one({"translation.inputLanguage": input_language}) is not None
        assert get_translations_collection(mongo_client).find_one({"translation.inputLanguage": "zh"}) is None

    def test_get_users_collection(self, mongo_client):
        users_collection = get_users_collection(mongo_client)
        assert users_collection.find_one({"name": "admin"}) is not None
        assert users_collection.find_one({"name": "user"}) is None
        
    # Routes:
    # noauth - User not logged in & cannot see restricted pages
    def test_noauth_login(self, client):
        # Ensure user is logged out
        response = client.get("/record")
        assert response.status_code == 302
        assert response.request.path == "/login"

        response = client.get("/history")
        assert response.status_code == 302
        assert response.request.path == "/login"

        # Test the logged out /login page
        response = client.get("/login")
        assert response.status_code == 200
        assert "Login" in response.data
    
    def test_noauth_homepage(self, client):
        # Test the logged out /register page
        response = client.get("/")
        assert response.status_code == 200
        assert "Translate Anything" in response.data

    def test_noauth_register(self, client):
        # Test the logged out /register page
        response = client.get("/register")
        assert response.status_code == 200
        assert "Register" in response.data
    
    def test_noauth_record(self, client):
        # Test for redirect to /login
        response = client.get("/record")
        assert response.status_code == 302
        assert response.request.path == "/login"
    
    def test_noauth_history(self, client):
        # Test for redirect to /login
        response = client.get("/history")
        assert response.status_code == 302
        assert response.request.path == "/login"

    def test_user_login(self, client):
        # Test logging in the user
        response = client.post("/login", data={
            "email": "admin",
            "password": "adminpassword",
        })
        assert response.status_code == 200
    
    # auth - User logged in & can see restricted pages
    def test_auth_login(self, client):
        # Test for redirect to home
        response = client.get("/login")
        assert response.status_code == 302
        assert response.request.path == "/"

    def test_auth_register(self, client):
        # Test for redirect to home
        response = client.get("/register")
        assert response.status_code == 302
        assert response.request.path == "/"
    
    def test_auth_record(self, client):
        # Test for content on home page
        response = client.get("/record")
        assert response.status_code == 200
        assert "Audio Recorder" in response.data

    def test_auth_history(self, client):
        # Test for content on history page
        response = client.get("/history")
        assert response.status_code == 200
        assert "Translation History" in response.data
        assert "Guten tag." in response.data

    def test_logout():
        # Test logging the user out
        response = client.get("/logout")
        assert response.status_code == 302
        assert response.request.path == "/login"
        # Test that the user is logged out and can no longer access record page
        response = client.get("/record")
        assert response.status_code == 302
        assert response.request.path == "/login"

    def test_user_register(self, client, mongo_client):
        response = client.post("/register", data={
            "email": "admin1",
            "password": "adminpassword1",
            "confirm": "adminpassword1"
        })
        # redirect to login upon successful registration
        assert response.status_code == 302
        # Check DB to see if entry was added
        users_collection = get_users_collection(mongo_client)
        assert users_collection.find_one({"name": "admin1"}) is not None