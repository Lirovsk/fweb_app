import functools
from flask import (Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from .Engines.EngineCreation import create_engine, retrieve_engine

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('create-room', methods=('GET', 'POST'))
def create_room():
    if request.method == 'POST':
        game_name = request.form['name']
        game_pin = request.form['pin']
        error = None
        
        session['game_name'] = game_name
        session['game_pin'] = game_pin
        
        if not game_name:
            error = 'Game name is required.'
        elif not game_pin:
            error = 'Game pin is required.'
        elif len(game_pin) != 4:
            error = 'Game pin must be 4 characters long.'
        
        if error is None:
            try:
                create_engine(game_name, game_pin)
                return redirect(url_for('auth.direct_room'))
            except Exception as e:
                error = f"Error creating game room: {e}"
        
        flash(error)
    
    return render_template('General_registration/create_gameRoom.html')

@bp.route('direct-room', methods=('GET', 'POST'))
def direct_room():
    if request.method == 'POST':
        game_name = session['game_name']
        game_pin = session['game_pin']

        user_name = request.form['user_name']
        user_pin = request.form['user_pin']
        
        if not game_name or not game_pin:
            flash('No game room created yet.')
            return redirect(url_for('auth.create_room'))
        
        game = retrieve_engine(game_name)
    else:
        game = retrieve_engine(session['game_name'])
        # Logic to enter the game room goes here
    return render_template('General_registration/NewPlayer.html', game=game)
