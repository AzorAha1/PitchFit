#!/usr/bin/python3
from flask import Flask, render_template

app = Flask(__name__, template_folder='../frontend/templates/', static_folder='../frontend/')

@app.route('/')
def landingpage():
    """This is the landing page"""
    return render_template('index.html', title='Home')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

