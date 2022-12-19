from app import create_app
from app.db import get_translations_collection, get_users_collection, insert_sample_data
from flask import session
import pytest
import mongomock
import os

class Tests: # pragma: no cover
    @pytest.fixture
    def mongo_client(self):
        mock_client = mongomock.MongoClient('mongodb://localhost:27017')
        mock_users_collection = mock_client.translator.users
        mock_users_collection.insert_one({
            "_id": "634f028fa11c10159ae12606",
            "name": "admin",
            "password": "adminpassword"
        })
        mock_translations_collection = mock_client.translator.translations
        mock_translations_collection.insert_one({
            "_id": "634f028fa11c10159ae12606",
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
        mongo_client.translator.translations.drop()
        assert get_users_collection(mongo_client).find_one({"name":"admin"}) is None
        assert get_users_collection(mongo_client).find_one({"translation.inputLanguage":"de"}) is None

        dir_path = os.path.dirname(os.path.realpath(__file__))
        user_data_path = os.path.join(dir_path, './sample_user_data.json')
        translation_data_path = os.path.join(dir_path, './sample_translation_data.json')
        insert_sample_data(mongo_client, user_data_path, translation_data_path)

        assert get_users_collection(mongo_client).find_one({"name":"admin"}) is not None
        assert get_translations_collection(mongo_client).find_one({"translation.inputLanguage":"de"}) is not None

    def test_get_translations_collection(self, mongo_client):
        input_languages = ["de"]
        for input_language in input_languages:
            assert get_translations_collection(mongo_client).find_one({"translation.inputLanguage": input_language}) is not None
        assert get_translations_collection(mongo_client).find_one({"translation.inputLanguage": "zh"}) is None

        output_languages = ["en"]
        for output_language in output_languages:
            assert get_translations_collection(mongo_client).find_one({"translation.outputLanguage": output_language}) is not None
        assert get_translations_collection(mongo_client).find_one({"translation.outputLanguage": "zh"}) is None

    def test_get_users_collection(self, mongo_client):
        assert get_users_collection(mongo_client).find_one({"name": "admin"}) is not None
        assert get_users_collection(mongo_client).find_one({"name": "user"}) is None
        
    # Routes:
    # noauth - User not logged in & cannot see restricted pages
    def test_noauth_login(self, client):
        # Ensure user is logged out
        response = client.get("/history")
        assert response.status_code == 302
        response = client.get("/history", follow_redirects=True)
        assert response.request.path == "/login"

        # Test the logged out /login page
        response = client.get("/login")
        assert response.status_code == 200
        assert b"Login" in response.data
    
    def test_noauth_homepage(self, client):
        # Test the logged out /register page
        response = client.get("/")
        assert response.status_code == 200
        assert b"Translate Anything" in response.data
    
    def test_noauth_record(self, client):
        # Test for content on home page
        response = client.get("/record")
        assert response.status_code == 200
        assert b"Audio Recorder" in response.data

    def test_noauth_register(self, client):
        # Test the logged out /register page
        response = client.get("/register")
        assert response.status_code == 200
        assert b"Register" in response.data
    
    def test_noauth_history(self, client):
        # Test for redirect to /login
        response = client.get("/history")
        assert response.status_code == 302
        response = client.get("/history", follow_redirects=True)
        assert response.request.path == "/login"

    # Test user auth functionality
    def test_user_register(self, client, mongo_client):
        # Test registering the user
        response = client.post("/register", data={
            "email": "admin1",
            "password": "adminpassword1",
            "confirm": "adminpassword1"
        })
        # redirect to login upon successful registration
        assert response.status_code == 302

    def test_user_login(self, client):
        # Test logging in the user
        with client:
            response = client.post("/register", data={
                "email": "admin1",
                "password": "adminpassword1",
                "confirm": "adminpassword1"
            })
            response = client.post("/login", data={
                "email": "admin1",
                "password": "adminpassword1",
            })
            assert response.status_code == 302
            assert 'uid' in session
    
    # auth - User logged in & can see restricted pages
    def test_auth_login(self, client):
        # Simulate user login
        with client.session_transaction() as session:
            session["uid"] = 1
        # Test for redirect to home
        response = client.get("/login")
        assert response.status_code == 302
        response = client.get("/login", follow_redirects=True)
        assert response.request.path == "/record"

    def test_auth_register(self, client):
        # Simulate user login
        with client.session_transaction() as session:
            session["uid"] = 1
        # Test for redirect to home
        response = client.get("/register")
        assert response.status_code == 302
        response = client.get("/register", follow_redirects=True)
        assert response.request.path == "/record"

    def test_auth_history(self, client):
        # Simulate user login
        with client.session_transaction() as session:
            session["uid"] = 1
        # Test for content on history page
        response = client.get("/history")
        assert response.status_code == 200
        assert b"Translation History" in response.data

    def test_logout(self, client):
        with client:
            # First login
            response = client.post("/register", data={
                "email": "admin1",
                "password": "adminpassword1",
                "confirm": "adminpassword1"
            })
            response = client.post("/login", data={
                "email": "admin1",
                "password": "adminpassword1",
            })
            assert response.status_code == 302
            # Test logging the user out
            response = client.get("/logout", follow_redirects=True)
            assert response.request.path == "/login"
            # Test that the user is logged out and can no longer access record page
            response = client.get("/history")
            assert response.status_code == 302
            response = client.get("/history", follow_redirects=True)
            assert response.request.path == "/login"