from flask import Blueprint, render_template, current_app, session, redirect, url_for
from .auth import SESSION_VAR_NAME
import base64
from . import db

# ROUTING FOR MAIN/NON-AUTH PAGES

main = Blueprint('main', __name__)

@main.route('/')
def home():
    userid = "" if SESSION_VAR_NAME not in session else session[SESSION_VAR_NAME]
    return render_template('home.html', uid=userid)

@main.route('/history')
def history():
    # Check for if user is logged in
    if SESSION_VAR_NAME not in session:
        return redirect(url_for('auth.login'))

    # TODO: Use _id or username field to check for translations
    userid = session[SESSION_VAR_NAME]
    # only give us the list of translations for this user
    cursor = db.get_translations_collection(current_app.config['MONGO_CLIENT']).find({"user":userid}, {"translations" : 1})
    history_data = cursor["translations"]

    # From project 4 implementation

    return render_template('history.html', history=history_data)