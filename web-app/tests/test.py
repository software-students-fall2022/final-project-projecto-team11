from app import create_app, get_conn_str
from app.auth import logout_user
from app.db import get_translations_collection, insert_sample_data
import pytest
import mongomock
import os

class Tests: # pragma: no cover
    @pytest.fixture
    def mongo_client(self):
        mock_client = mongomock.MongoClient('mongodb://localhost:27017')
        mock_translations_collection = mock_client.translator.users
        mock_translations_collection.insert_one({
            "username": "admin",
            "password": "supersecurepassword",
            "translations": [
                {
                    "inputLanguage": "de",
                    "inputText": "Guten tag.",
                    "outputText": "Good morning.",
                    "outputLanguage": "en"
                },
                {
                    "inputLanguage": "es",
                    "inputText": "Mucho gusto.",
                    "outputText": "Nice to meet you.",
                    "outputLanguage": "en"
                },
                {
                    "inputLanguage": "fr",
                    "inputText": "Pardon, excusez-moi.",
                    "outputText": "Pardon, excuse me.",
                    "outputLanguage": "en"
                },
                {
                    "inputLanguage": "ja",
                    "inputText": "ごめんなさい。",
                    "outputText": "I am sorry.",
                    "outputLanguage": "en"
                }
            ]
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

    def test_get_connection_string(self):
        conn_str = get_conn_str()
        assert conn_str == 'mongodb://localhost:27017'
        os.environ["DB_USER"] = "dbadmin"
        os.environ["DB_PASS"] = "password"
        os.environ["DB_HOST"] = "127.0.0.1"
        conn_str = get_conn_str()
        assert conn_str == 'mongodb://dbadmin:password@127.0.0.1:27017'

    def test_insert_sample_data(self, mongo_client): 
        mongo_client.translator.users.drop()
        assert get_translations_collection(mongo_client).find_one({"username":"admin"}) is None

        dir_path = os.path.dirname(os.path.realpath(__file__))
        sample_data_path = os.path.join(dir_path, './sample_data.json')
        insert_sample_data(mongo_client, sample_data_path)

        assert get_translations_collection(mongo_client).find_one({"translations.inputLanguage":"de"}) is not None

    def test_get_translations_collection(self, mongo_client):
        translations_collection = get_translations_collection(mongo_client)
        input_languages = ["de", "es", "fr", "ja"]
        for input_language in input_languages:
            assert get_translations_collection(mongo_client).find_one({"translations.inputLanguage": input_language}) is not None
        assert get_translations_collection(mongo_client).find_one({"translations.inputLanguage": "zh"}) is None

    def test_logged_out_routes(self, client):
        # TODO: Log client in
        logout_user()
        # TODO: Check the actual response data
        response = client.get("/login")
        assert response.status_code == 200
        response = client.get("/register")
        assert response.status_code == 200

    def test_logged_out_routes(self, client):
        # TODO: Log the client in
        # TODO: Check the actual response data
        response = client.get("/")
        assert response.status_code == 200
        response = client.get("/history")
        assert response.status_code == 200
        response = client.get("/logout")
        # TODO: Check that the client was correctly redirected

    def test_translation_endpoint_update(self, client, mongo_client):
        response1 = client.get("/history")
        #assert b'"inputLanguage":"ja"' in response1.data
        assert b'"inputLanguage":"zh"' not in response1.data

        mongo_client.translator.translations.insert_one({
            "inputLanguage": "zh",
            "inputText": "不用谢。",
            "outputText": "You're welcome."
        })

        response2 = client.get("/history")
        # TODO: test actual update once data is populated on history page
        # assert b'"inputLanguage":"zh"' in response2.data
        # assert b'"inputLanguage":"ja"' not in response2.data