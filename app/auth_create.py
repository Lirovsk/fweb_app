import functools
from flask import (Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from .Engines.EngineCreation import create_engine_data, retrieve_engine_data
from .Engines.RoomCreation import create_game_room, check_existing_room
from .Engines.CreatingUser import creating_user
from .Engines import GeneralServices as services

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/setting-room/<gameType>')
def setting_room(gameType):
    session['game_type'] = gameType
    return redirect(url_for('auth.create_room'))

@bp.route('create-room', methods=('GET', 'POST'))
def create_room():
    if request.method == 'POST':
        game_name = request.form['name']
        game_pin = request.form['pin']
        error = None
        
        session['game_name'] = game_name
        session['game_pin'] = game_pin
        game_type = session.get('game_type')
        if not game_name:
            error = 'Game name is required.'
        elif not game_pin:
            error = 'Game pin is required.'
        elif len(game_pin) != 4:
            error = 'Game pin must be 4 characters long.'
        
        if error is None:
            try:
                create_engine_data(game_type, game_name, game_pin)
                create_game_room(game_name)
                session['game_created'] = True
                return redirect(url_for('auth.direct_room'))
            except Exception as e:
                error = f"Error creating game room: {e}"
        session.clear()
        flash(error)
    
    return render_template('General_registration/create_gameRoom.html')

@bp.route('/direct-room', methods=['GET', 'POST'])
def direct_room():
    if request.method == 'POST':
        game_name = session['game_name']
        game_pin = session['game_pin']

        user_name = request.form['user_name']
        user_pin = request.form['user_pin']
        
        if not game_name or not game_pin:
            flash('No game room created yet.')
            return redirect(url_for('auth.create_room'))
        
        game = retrieve_engine_data(game_name)
        
        if session['game_created'] is False:
            # replace this part with some logic that verifies is the table of the room exists
            try:
                create_game_room(game_name)
            except Exception as e:
                flash(f"Error creating game room: {e}")
            session['game_created'] = True
            

        user = creating_user(user_name, user_pin, game_name)
        session['user_name'] = user_name
        session['user_pin'] = user_pin
        return redirect(url_for('room.gameRoom'))
    else:
        game = retrieve_engine_data(session['game_name'])
        if game[0] is False:
            flash(game[1])
            return redirect(url_for('auth.create_room'))

    return render_template('General_registration/NewPlayer.html', game=game[1])


@bp.route('enter-room', methods=['GET', 'POST'])
def enterRoom():
    session.clear()
    error = None

    if request.method == 'POST':
        # Getting the data from the user
        game_name = request.form['game_room']
        game_pin = request.form['game_pin']
        user_name = request.form['user_name']
        user_pin = request.form['user_pin']

        # Checking if all the data is present
        result = services.check_existing(game_name=game_name, game_pin=game_pin, user_name=user_name, user_pin=user_pin)
        if result['trial'] == False:
            flash(result['message'])
            return redirect(url_for('auth.enterRoom'))    
        
        # Storing the data in the session
        session['game_name'] = game_name
        session['game_pin'] = game_pin

        # Checking if the game room exists and if the pin is correct
        engine_check = retrieve_engine_data(game_name) # changed
        if engine_check[0] == False:
            flash(engine_check[1])
            return redirect(url_for('auth.create_room'))
        
        room_result = check_existing_room(game_name) # changed
        if room_result[0] == True:
            if room_result [1] == False:
                create_game_room(game_name)
        else:            
            flash(room_result[1])
            return redirect(url_for('auth.create_room'))

        
        # checking if the pin is correct
        if engine_check[0] == True: #checked
            if engine_check[1].pin != game_pin: #linha 107
                flash('Incorrect game pin.')
                return redirect(url_for('auth.enterRoom'))
    
        user = creating_user(user_name, user_pin, game_name)
        session['user_name'] = user_name
        session['user_pin'] = user_pin
        session['user_balance'] = user.balance
        return redirect(url_for('room.gameRoom'))

    return render_template('General_registration/NewPlayerNogame.html')