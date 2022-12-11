from flask import Flask
from flask_cors import CORS
import pymongo
import translator.endpoints
import translator.jobhandler
import translator.util
import os

def create_app(test_config=None):
    # Create flask app.
    app = Flask(__name__)
    CORS(app)

    # Default number of whisper threads to start up.
    # NOTE: I only had enough RAM for 2 threads at once, and my CPU was pinned when 
    NUM_THREADS = 2

    # Get MongoDB connection string.
    if (test_config == None):
        conn_str = os.getenv('DB_URL', 'mongodb://localhost:27017')
        app.config.from_mapping(MONGO_CLIENT=pymongo.MongoClient(conn_str), NUM_THREADS=NUM_THREADS)
    else:
        app.config.from_mapping(test_config)
    
    # Connect to the database and start whisper threads.
    translator.jobhandler.start_threads(app.config['NUM_THREADS'], translator.util.get_db())

    # Set up endpoints.
    app.add_url_rule('/translation', methods=["POST"], view_func=translator.endpoints.add_job)
    app.add_url_rule('/translation/<id>', methods=["GET", "POST"], view_func=translator.endpoints.get_job)

    return app
