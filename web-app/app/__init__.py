from flask import Flask, render_template, Blueprint
from pymongo import MongoClient
import os

def create_app(test_config=None):
    app = Flask(__name__)

    # Set up DB
    if test_config is None:
        app.config.from_mapping(
            MONGO_CLIENT=MongoClient(get_conn_str())
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

# Generates connection string from env vars
def get_conn_str():
    # optional db auth and options
    db_user = os.getenv('DB_USER', '')
    db_pass = os.getenv('DB_PASS', '')
    db_user_pass = f'{db_user}:{db_pass}@' if db_user else ''
    # optional options ex: '/?authSource=admin'
    db_opts = os.getenv('DB_OPTS', '')
    # required host and port
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '27017')
    return f'mongodb://{db_user_pass}{db_host}:{db_port}'