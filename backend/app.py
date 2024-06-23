#!/usr/bin/python3
from flask import Flask, render_template

app = Flask(__name__, template_folder='../frontend/templates/', static_folder='../frontend/')

@app.route('/')
def landingpage():
    """This is the landing page"""
    return render_template('index.html', title='Home')
@app.route('/signin')
def sigin():
    """this is the sign in page"""
    return render_template('signin.html', title='Sign In')
@app.route('/signup')
def signup():
    """this is the sign up page"""
    return render_template('signup.html', title='Sign Up')
if __name__ == '__main__':
    app.run(debug=True, port=5001)

