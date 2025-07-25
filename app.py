from flask import Flask, url_for, render_template, request, redirect, session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from logic.Engines.EngineCreation import create_engine, retrieve_engine
from logic.Engines.RoomCreation import create_game_room
from logic.Engines.CreatingUser import creating_user
from logic.Engines.services import retrieving_players, retrieving_one_player

app = Flask(__name__)
app.secret_key = '8289488e3c541c0c0088797d84dfaaa0d3802941c593f870645df79a1d5346a9'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game')
def game_home():
    return render_template('game.html')

@app.route('/create_engines')
def create_engines():
    return render_template('create_gameRoom.html')

@app.route('/create_engines/', methods=['POST'])
def create_game():
    name = request.form['name']
    pin = request.form['pin']
    session['room_name'] = name
    session['pin'] = pin
    if not name or not pin:
        return "Name and PIN are required", 400
    
    try:
        newEngine = create_engine(name, pin)
    except Exception as e:
        return f"Error creating game: {e}", 500
    create_game_room(newEngine.room_name)
    return render_template('NewPlayer.html', game=newEngine)

@app.route('/create_engines/enterDirectRoom', methods=['GET'])
def enter_direct_room():
    session.clear()
    return render_template('NewPlayerNogame.html', game=None)

@app.route('/create_engines/room/', methods=['POST'])
def enterRoom():
    user_name = request.form['user_name']
    pin = request.form['pin']
    room_name = request.form['room_name']
    player = retrieving_one_player(room_name, user_name)
    if player is not None:
        session['user_name'] = player.user_name
        session['user_pin'] = player.pin
        session['room_name'] = room_name
    
        return redirect(url_for('gameRoom'))
    user = creating_user(user_name, pin, room_name)
    session['user_name'] = user.user_name
    session['user_pin'] = user.pin
    session['room_name'] = room_name
    
    # Logic to handle entering the room
    return redirect(url_for('gameRoom'))


@app.route('/create_engines/room/')
def gameRoom():
    room_name = session['room_name']
    game = retrieve_engine(room_name)
    players = retrieving_players(room_name)

    return render_template('enter_game.html', game=game, players=players)

@app.route('/create_engines/room/payment')
def payment():
    room_name = session['room_name']
    game = retrieve_engine(room_name)
    players = retrieving_players(room_name)

    return render_template('payment.html', game=game, players=players)