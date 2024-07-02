#!/usr/bin/python3
from bson import ObjectId
from flask import Flask, flash, render_template, request, redirect, session, url_for
import bcrypt
from flask_pymongo import PyMongo
from foodstorageapi import foodapi

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
                user['_id'] = str(user['_id'])
                session['user'] = user
                return redirect('/dashboard')
        error_message = 'Invalid Credentials'
        flash(error_message)
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
        # session['user']['name'] = request.form['preferred_name']
        # session['user']['weight'] = request.form['weight']
        # session['user']['height'] = request.form['height']
        # session['user']['gender'] = request.form['gender']
        # session['user']['age'] = request.form['age']
        existing_user = mongo.db.users.find_one({'$or': [{'username': session['user']['username']}, {'email': session['user']['email']}]})
        if existing_user:
            print("User already exists")  # Debugging line
            return 'Username or Email Already Exists'

        # using bcrpyt to hash password
        session['user']['password'] = bcrypt.hashpw(session['user']['password'].encode('utf-8'), bcrypt.gensalt())
        result = mongo.db.users.insert_one(session['user'])
        session['user']['_id'] = str(result.inserted_id) 
        return redirect(url_for('getname'))  
    return render_template('signup.html', title='Sign Up')

@app.route('/signup/step1', methods=['GET', 'POST'])
def getname():
    """step 1 of setup"""
    if request.method == 'POST':
        print(f"{request.form['preferred_name']}")
        session['user']['name'] = request.form['preferred_name']
        mongo.db.users.update_one({'username': session['user']['username']}, {'$set': {'name': session['user']['name']}})
        return redirect(url_for('getage'))
    return render_template('setup1.html', title='Setup Step 1')

@app.route('/signup/step2', methods=['GET', 'POST'])
def getage():
    """step 2 of setup"""
    if request.method == 'POST':
        print(f"{request.form['age']}")
        session['user']['age'] = request.form['age']
        mongo.db.users.update_one({'username': session['user']['username']}, {'$set': {'age': session['user']['age']}})
        return redirect(url_for('getweight'))
    return render_template('setup2.html', title='Setup Step 2')

@app.route('/signup/step3', methods=['GET', 'POST'])
def getweight():
    """step 3 of setup"""
    if request.method == 'POST':
        print(f"{request.form['weight']}")
        session['user']['weight'] = request.form['weight']
        mongo.db.users.update_one({'username': session['user']['username']}, {'$set': {'weight': session['user']['weight']}})
        return redirect(url_for('getheight'))
    return render_template('setup3.html', title='Setup Step 3')

@app.route('/signup/step4', methods=['GET', 'POST'])
def getheight():
    """step 4 of setup"""
    if request.method == 'POST':
        print(f"{request.form['height']}")
        session['user']['height'] = request.form['height']
        mongo.db.users.update_one({'username': session['user']['username']}, {'$set': {'height': session['user']['height']}})
        return redirect(url_for('getgender'))
    return render_template('setup4.html', title='Setup Step 4')

@app.route('/signup/step5', methods=['GET', 'POST'])
def getgender():
    """get the gender of user"""
    if request.method == 'POST':
        session['user']['gender'] = request.form['gender']
        print(f"{request.form['gender']}")
        mongo.db.users.update_one({'username': session['user']['username']}, {'$set': {'gender': session['user']['gender']}})
        return redirect(url_for('goals'))
    return render_template('getgender.html', title='Gender')

@app.route('/signup/weight_loss', methods=['GET', 'POST'])
def weight_loss():
    """page for weight loss"""
    if request.method == 'POST':
        if request.form['weight_loss_complete'] == 'true':
            return redirect(url_for('deficit'))
    return render_template('weight_loss.html', title='Weight Loss')

@app.route('/signup/goals', methods=['GET', 'POST'])
def goals():
    """setting goals"""
    if request.method == 'POST':
        if 'selected_goals' in request.form:
            session['user']['goals'] = request.form['selected_goals']
            # mongo.db.users.insert_one(session['user'])
            
            print(f'The Goals are: {session["user"]["goals"]}')
            goals = session['user']['goals']
            mongo.db.users.update_one({'username': session['user']['username']}, {'$set': {'goals': session['user']['goals']}})
            if 'Weight Loss' in goals:
                return redirect(url_for('deficit'))
            return redirect(url_for('dashboard'))
        else:
            print("Error: 'selected_goals' key not found in form data.")
    print(f'The User is: {session["user"]}')
    return render_template('goals.html', title='Goals')

@app.route('/signup/deficit', methods=['GET', 'POST'])
def deficit():
    """This is the step to calculate calorie deficit"""
    if request.method == 'POST':
        # Check if 'calories_deficit' is in the form data
        if 'calories_deficit' in request.form:
            if request.form['calories_deficit'] == 'true':
                session['user']['calories_deficit'] = True
                return redirect(url_for('dashboard'))
            else:
                session['user']['calories_deficit'] = False
        else:
            # Handle the case where 'calories_deficit' is not in the form data
            session['user']['calories_deficit'] = False  

    
    user = mongo.db.users.find_one({'_id': ObjectId(session['user']['_id'])})
    weight = float(user['weight'])
    height = float(user['height'])
    age = int(user['age'])
    gender = user['gender']
    
    if gender == 'male':
        bmr = 66 + (6.2 * weight) + (12.7 * height) - (6.76 * age)
    else:
        bmr = 655 + (4.35 * weight) + (4.7 * height) - (4.7 * age)
    
    tdee = bmr * 1.2  # Assuming a sedentary lifestyle by default
    session['user']['bmr'] = bmr
    session['user']['tdee'] = tdee

    # Update the user document in MongoDB
    mongo.db.users.update_one(
        {'username': session['user']['username']},
        {'$set': {'bmr': bmr, 'tdee': tdee}}
    )
    
    print(f'BMR: {bmr}')
    print(f'TDEE: {tdee}')
    
    return render_template('caloriesdeficit.html', title='Calorie Deficit', bmr=bmr, tdee=tdee)


@app.route('/dashboard')
def dashboard():
    """this is the dashboard page"""
    user_id = session.get('user', {}).get('_id')
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return redirect(url_for('signin'))
    # convert objectid to string for json serialization 
    user['_id'] = str(user['_id'])
    return render_template('dashboard.html', title='Dashboard', user=user)
@app.route('/dashboard/workout')
def workout():
    """this is where the work out plan will be"""
    user_id = session.get('user', {}).get('_id')
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return redirect(url_for('signin'))
    # convert objectid to string for json serialization 
    user['_id'] = str(user['_id'])
    return render_template('workout.html', title='Workout', user=user)
@app.route('/dashboard/addfood', methods=['GET', 'POST'])
def addfood():
    """this is where to log meals"""
    user_id = session.get('user', {}).get('_id')
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return redirect(url_for('signin'))
    # convert objectid to string for json serialization 
    user['_id'] = str(user['_id'])
    return render_template('addfood.html')
@app.route('/debug/users')
def debug_users():
    """Route to debug user data in MongoDB"""
    users = mongo.db.users.find()
    users_list = list(users)
    return render_template('debug_users.html', users=users_list)

@app.route('/signout')
def signout():
    """this is the signout page"""
    session.pop('user', None)
    print('User has been signed out')
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
