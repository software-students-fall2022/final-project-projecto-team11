import pymongo
import json
import sys

# Get all users data for client (user mapped to list of translations)
def get_translations_collection(client):
    db = client.translator
    return db.users

# Insert sample data into DB for testing
def insert_sample_data(client, fn='sample_data.json'):
    with open(fn, 'r', encoding='utf-8') as f:
        data = json.load(f)
        get_translations_collection(client).insert_many(data)

if __name__ == "__main__":
    # import sample data into the database
    if len(sys.argv) > 1:
        insert_sample_data(pymongo.MongoClient('mongodb://localhost:27017'), sys.argv[1])
    else:
        insert_sample_data(pymongo.MongoClient('mongodb://localhost:27017'))