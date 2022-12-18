from app import create_app, get_conn_str
from app.auth import logout_user
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
        # TODO: Ensure user is logged out
        # TODO: Test the logged out /login page
        assert True

    def test_noauth_register(self, client):
        # TODO: Test the logged out /register page
        assert True
    
    def test_noauth_home(self, client):
        # TODO: Test for redirect to /login
        assert True
    
    def test_noauth_history(self, client):
        # TODO: Test for redirect to /login
        assert True

    def test_user_login(self, client):
        # TODO: Test logging in the user
        assert True
    
    # auth - User logged in & can see restricted pages
    def test_auth_login(self, client):
        # TODO: Test for redirect to home
        assert True

    def test_auth_register(self, client):
        # TODO: Test for redirect to home
        assert True
    
    def test_auth_home(self, client):
        # TODO: Test for content on home page
        assert True

    def test_auth_history(self, client):
        # TODO: Test for content on history page
        assert True

    def test_logout():
        # TODO: Test logging the user out
        assert True