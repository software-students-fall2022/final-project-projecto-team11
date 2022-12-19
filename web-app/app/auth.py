from flask import Blueprint, render_template, request, current_app, redirect, url_for, session
from . import db
import bcrypt

auth = Blueprint('auth', __name__)

SESSION_VAR_NAME = 'uid'

@auth.route('/login-error')
def loginerror():
    return render_template('login-fail-page.html')

@auth.route('/login', methods=['GET'])
def login():
    # If user is logged in, redirect them to home page:
    if SESSION_VAR_NAME in session:
        return redirect(url_for('main.record'))
    # Otherwise, give them the login form HTML template.
    return render_template('login-page.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    # If information not present, redirect back to login screen.
    if email == None or password == None:
        return redirect(url_for('auth.loginerror'))

    # Search for a user in the database with matching username.
    dbuserentry = db.get_users_collection(current_app.config['MONGO_CLIENT']).find_one({"username": email})

    # Check if user is null, if so redirect.
    if dbuserentry == None:
        return redirect(url_for('auth.loginerror'))

    # Check provided password matches password stored in the database.
    if not bcrypt.checkpw(password.encode('utf8'), dbuserentry['password']):
        return redirect(url_for('auth.loginerror'))
    
    # If everything matches, send logged-in user to the home page.
    # Use this user ID to create a session
    session[SESSION_VAR_NAME] = str(dbuserentry['_id'])
    return redirect(url_for('main.record'))

@auth.route('/register', methods=['GET'])
def register():
    # If user is logged in, send them to the home page.
    if SESSION_VAR_NAME in session:
        return redirect(url_for('main.record'))
    
    # Otherwise, give them the registration form page.
    return render_template('register-page.html')

@auth.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    # If information not present or not correct, redirect back to login screen.
    if email == None or password == None or confirm == None or password != confirm:
        return redirect(url_for('auth.register'))

    # Check to make sure user doesn't already exist with the given email.
    if db.get_users_collection(current_app.config['MONGO_CLIENT']).count_documents({"username": email}) > 0:
        # User with email already exists.
        return redirect(url_for('auth.register'))

    # If we've made it to this point, it's safe to create the user.
    db.get_users_collection(current_app.config['MONGO_CLIENT']).insert_one({
        'username': email,
        'password': bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    })

    # Once the user has been successfully created, redirect them to the login page.
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    # Check if user is logged in. If user is not logged in, redirect them to the login page.
    if SESSION_VAR_NAME not in session:
        return redirect(url_for('auth.login'))
    # If the user is logged in, end their session (log them out).
    session.clear()
    return redirect(url_for('auth.login'))