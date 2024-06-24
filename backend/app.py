#!/usr/bin/python3
from flask import Flask, render_template, request, redirect
import bcrypt
from flask_pymongo import PyMongo

app = Flask(__name__, template_folder='../frontend/templates/', static_folder='../frontend/')
app.config['MONGO_URI'] = 'mongodb://localhost:27017/pitchfitdb'
mongo = PyMongo(app)
@app.route('/')
def landingpage():
    """This is the landing page"""
    return render_template('index.html', title='Home')
@app.route('/signin')
def signin():
    """this is the sign in page"""
    return render_template('signin.html', title='Sign In')
@app.route('/signup')
def signup():
    """this is the sign up page"""
    if request.form == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        existing_user = mongo.db.users.find_one({'$or': [{'username': username}, {'email': email}]})
        if existing_user:
            return 'Username or Email Already Exists'

        # using bcrpyt to hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'password': hashed_password
        }
        mongo.db.users.insert_one(user)
        redirect('/signin')
    return render_template('signup.html', title='Sign Up')
if __name__ == '__main__':
    app.run(debug=True, port=5001)

