from flask import Flask, render_template, Blueprint
from pymongo import MongoClient
import os

def create_app(test_config=None):
    app = Flask(__name__)

    # Set up DB
    if test_config is None:
        db_conn_str = os.getenv('DB_URL', 'mongodb://localhost:27017')
        app.config.from_mapping(
            MONGO_CLIENT=MongoClient(db_conn_str)
        )
    else:
        app.config.from_mapping(test_config)

    # Routing
    app.static_folder = 'static'

    # blueprint for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app