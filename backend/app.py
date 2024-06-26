#!/usr/bin/python3
from flask import Flask, render_template, request, redirect
import bcrypt
from flask_pymongo import PyMongo

app = Flask(__name__, template_folder='../frontend/templates/', static_folder='../frontend/')
app.secret_key = 'youwillneverfindoutwhatthisis'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/pitchfitdb'
mongo = PyMongo(app)
@app.route('/')
def landingpage():
    """This is the landing page"""
    return render_template('index.html', title='Home')
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """this is the sign in page"""
    error_message = None
    if request.method == 'POST':
        print("Form data received")
        username = request.form['username']
        password = request.form['password']
        user = mongo.db.users.find_one({'username': username})
        if user:
            rehashed_password = bcrypt.checkpw(password.encode('utf-8'), user['password'])
            if rehashed_password:
                print(f'User {username} has been authenticated')
                return redirect('/dashboard')
        error_message = 'Invalid Credentials'
    return render_template('signin.html', title='Sign In', error=error_message)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """this is the sign up page"""
    if request.method == 'POST':
        print("Form data received")  # Debugging line
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        existing_user = mongo.db.users.find_one({'$or': [{'username': username}, {'email': email}]})
        if existing_user:
            print("User already exists")  # Debugging line
            return 'Username or Email Already Exists'

        # using bcrpyt to hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = {
            'email': email,
            'username': username,
            'password': hashed_password
        }
        mongo.db.users.insert_one(user)
        print(f'User {username} has been created')
        return redirect('/setup/step1')
    return render_template('signup.html', title='Sign Up')
@app.route('/signup/step1', methods=['GET', 'POST'])
def getname():
    """step 1 of setup"""
    return render_template('setup1.html', title='Setup Step 1')
@app.route('/signup/step2', methods=['GET', 'POST'])
def getage():
    """step 2 of setup"""
    return render_template('setup2.html', title='Setup Step 2')
@app.route('/signup/step3', methods=['GET', 'POST'])
def getweight():
    """step 3 of setup"""
    return render_template('setup3.html', title='Setup Step 3')
@app.route('/signup/step4', methods=['GET', 'POST'])
def getheight():
    """step 4 of setup"""
    return render_template('setup4.html', title='Setup Step 4')
@app.route('/signup/goals', methods=['GET', 'POST'])
def goals():
    """setting goals"""
    if request.method == 'POST':
        try:
            thegoals = request.form['selected_goals']
            print(f'The Goals are: {thegoals}')
        except KeyError:
            print("The 'selected_goals' key was not found in the form data.")
    return render_template('goals.html', title='Goals')
@app.route('/dashboard')
def dashboard():
    """this is the dashboard page"""
    return render_template('dashboard.html', title='Dashboard')
if __name__ == '__main__':
    app.run(debug=True, port=5001)

