import pymongo

def get_db():
    try:
        client = pymongo.MongoClient('mongodb://localhost:27017')
        db = client.get_database('translator')
        return pymongo.collection.Collection(db, 'translations')
    except pymongo.errors.ConnectionFailure as e:
        print("MongoDB server connection error.")
    except Exception as e:
        print(e)

db = get_db()

supported_languages = ["fr", "es", "hi", "de"]
