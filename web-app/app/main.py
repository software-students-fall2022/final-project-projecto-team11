from flask import Blueprint, render_template, current_app
from . import db

# ROUTING FOR MAIN/NON-AUTH PAGES

main = Blueprint('main', __name__)

# TODO: Require login to access this page
@main.route('/')
def home():
    # TODO: Set up check for if user is logged in
    if False:
        return redirect(url_for('auth.login'))
    return render_template('home.html')

# TODO: Require login to access this page
@main.route('/history')
def history():
    # TODO: Set up check for if user is logged in
    if False:
        return redirect(url_for('auth.login'))

    # TODO: Use _id or username field to check for translations
    username_or_id = "admin"
    # only give us the list of translations for this user
    cursor = db.get_translations_collection(current_app.config['MONGO_CLIENT']).find_one({"username":username_or_id}, {"translations" : 1})
    history_data = cursor["translations"]

    # From project 4 implementation

    return render_template('history.html', history=history_data)