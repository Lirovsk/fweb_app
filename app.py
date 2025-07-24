from flask import Flask, url_for, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_engines', methods=['GET'])
def create_engines():
    pass

@app.route('/engines', methods=['POST'])
def create_game():
    pass

@app.route('/engines/<name>')
def enterRoom(name):
    pass
    