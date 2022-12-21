import pymongo
import os

def get_db():
    try:
        conn_str = os.getenv('DB_URL', 'mongodb://localhost:27017')
        client = pymongo.MongoClient(conn_str)
        db = client.get_database('translator')
        return pymongo.collection.Collection(db, 'translations')
    except pymongo.errors.ConnectionFailure as e:
        print("MongoDB server connection error.")
    except Exception as e:
        print(e)

db = get_db()

supported_languages = ["fr", "es", "hi", "de"]
