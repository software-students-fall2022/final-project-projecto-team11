import pymongo
import json
import sys

# Returns users collection given client
def get_users_collection(client):
    try:
        db = client.get_database('translator')
        return pymongo.collection.Collection(db, 'users')
    except Exception as e:
        print(f"Error getting translation collection: {e}")
        return None

# Returns translations collection given client
def get_translations_collection(client):
    try:
        db = client.get_database('translator')
        return pymongo.collection.Collection(db, 'translations')
    except Exception as e:
        print(f"Error getting translation collection: {e}")
        return None

# Insert sample data into DB for testing
def insert_sample_data(client, user_fn='sample_user_data.json', translation_fn='sample_translation_data.json'):
    try:
        user_file = open(user_fn, 'r', encoding='utf-8')
        translation_file = open(translation_fn, 'r', encoding='utf-8')
        user_data = json.load(user_file)
        translation_data = json.load(translation_file)
        get_users_collection(client).insert_many(user_data)
        get_users_collection(client).insert_many(translation_data)
    except FileNotFoundError:
        print("Could not find sample data file")
    except Exception as e:
        print(f"Error inserting sample data: {e}")

if __name__ == "__main__":
    # import sample data into the database
    if len(sys.argv) > 1:
        insert_sample_data(pymongo.MongoClient('mongodb://localhost:27017'), sys.argv[1])
    else:
        insert_sample_data(pymongo.MongoClient('mongodb://localhost:27017'))