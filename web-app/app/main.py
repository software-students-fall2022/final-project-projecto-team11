from flask import Blueprint, render_template, current_app, session, redirect, url_for
from .auth import SESSION_VAR_NAME
import base64
from . import db

# ROUTING FOR MAIN/NON-AUTH PAGES

main = Blueprint('main', __name__)

@main.route('/')
def landing():
    return render_template('homepage.html')

# TODO: Require login to access this page
@main.route('/record')
def record():
    userid = "" if SESSION_VAR_NAME not in session else session[SESSION_VAR_NAME]
    return render_template('audio-page.html', uid=userid)

@main.route('/history')
def history():
    # Check for if user is logged in
    if SESSION_VAR_NAME not in session:
        return redirect(url_for('auth.login'))

    # TODO: Use _id or username field to check for translations
    userid = session[SESSION_VAR_NAME]
    # only give us the list of translations for this user
    cursor = db.get_translations_collection(current_app.config['MONGO_CLIENT']).find({"user":userid}, {"translations" : 1})
    history_data = []
    # temporary fix - will have performance cost when larger amounts of data
    for doc in cursor:
        history_data.append(doc)

    message = ''
    if len(history_data) == 0:
        history_data = ''
        message = 'No translations complete yet. Record a translation to view translation history.'

    # From project 4 implementation

    return render_template('record-page.html', history=history_data, message=message)