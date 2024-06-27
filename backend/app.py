#!/usr/bin/python3
from flask import Flask, render_template, request, redirect, session, url_for
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
        # Process form data
        session['user'] = {}  # Initialize session user
        session['user']['email'] = request.form['email']
        session['user']['username'] = request.form['username']
        session['user']['password'] = request.form['password']

        existing_user = mongo.db.users.find_one({'$or': [{'username': session['user']['username']}, {'email': session['user']['email']}]})
        if existing_user:
            print("User already exists")  # Debugging line
            return 'Username or Email Already Exists'

        # using bcrpyt to hash password
        session['user']['password'] = bcrypt.hashpw(session['user']['password'].encode('utf-8'), bcrypt.gensalt())
        return redirect(url_for('getname'))  
    return render_template('signup.html', title='Sign Up')
@app.route('/signup/step1', methods=['GET', 'POST'])
def getname():
    """step 1 of setup"""
    if request.method == 'POST':
        session['user']['name'] = request.form['preferred_name']
        return redirect(url_for('getage'))
    return render_template('setup1.html', title='Setup Step 1')
@app.route('/signup/step2', methods=['GET', 'POST'])
def getage():
    """step 2 of setup"""
    if request.method == 'POST':
        session['user']['age'] = request.form['age']
        return redirect(url_for('getweight'))
    return render_template('setup2.html', title='Setup Step 2')
@app.route('/signup/step3', methods=['GET', 'POST'])
def getweight():
    """step 3 of setup"""
    if request.method == 'POST':
        session['user']['weight'] = request.form['weight']
        return redirect(url_for('getheight'))
    return render_template('setup3.html', title='Setup Step 3')
@app.route('/signup/step4', methods=['GET', 'POST'])
def getheight():
    """step 4 of setup"""
    if request.method == 'POST':
        session['user']['height'] = request.form['height']
        return redirect(url_for('goals'))
    return render_template('setup4.html', title='Setup Step 4')

@app.route('/signup/goals', methods=['GET', 'POST'])
def goals():
    """setting goals"""
    if request.method == 'POST':
        if 'selected_goals' in request.form:
            session['user']['goals'] = request.form['selected_goals']
            mongo.db.users.insert_one(session['user'])
            print(f'The Goals are: {session["user"]["goals"]}')
            goals = session['user']['goals']
           
            if 'Weight Loss' in goals:
                weight_loss_redirect = True
            else:
                weight_loss_redirect = False
            if weight_loss_redirect:
                return redirect(url_for('weight_loss'))
            return redirect(url_for('dashboard'))
        else:
            print("Error: 'selected_goals' key not found in form data.")
    return render_template('goals.html', title='Goals')

@app.route('/signup/weight_loss', methods=['GET', 'POST'])
def weight_loss():
    """page for weight loss"""
    if request.method == 'POST':
        if request.form['weight_loss_complete'] == 'true':
            return redirect(url_for('dashboard'))
    return render_template('weight_loss.html', title='Weight Loss')
@app.route('/dashboard')
def dashboard():
    """this is the dashboard page"""
    return render_template('dashboard.html', title='Dashboard')
@app.route('/signout')
def signout():
    """this is the signout page"""
    session.pop('user', None)
    print('User has been signed out')
    return redirect(url_for('signin'))
if __name__ == '__main__':
    app.run(debug=True, port=5001)

