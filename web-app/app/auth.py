from flask import Blueprint, render_template, request, redirect, url_for
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    # TODO: Set up check for if user is logged in
    if False:
        return redirect(url_for('main.home'))
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    # TODO: Authentication + log in user

    if True: # user auth failed
        return redirect(url_for('auth.login'))
    return redirect(url_for('main.home'))

@auth.route('/register')
def register():
    # TODO: Set up check for if user is logged in
    if False:
        return redirect(url_for('main.home'))
    
    return render_template('register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    if password != confirm:
        return redirect(url_for('auth.register'))

    # TODO: Create the user
    
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    # TODO: Set up check for if user is logged in
    if False:
        return redirect(url_for('auth.login'))
    # TODO: logout user
    return redirect(url_for('auth.login'))