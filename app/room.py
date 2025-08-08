import functools
from flask import (Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from .Engines.GeneralServices import retrieving_players

bp = Blueprint('room', __name__, url_prefix='/room')

def room_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'game_name' not in session:
            flash('You need to be in a game room first.')
            return redirect(url_for('auth.enterRoom'))
        elif 'user_name' not in session:
            flash('You need to enter your name first.')
            return redirect(url_for('auth.enterRoom'))
        return view(**kwargs)
    return wrapped_view

@bp.route('game-room', methods=['GET'])
@room_required
def gameRoom():
    error = None
    players = retrieving_players(session['game_name'])
    if players['trial'] == False:
        error = players['message']
        flash(error)
        return redirect(url_for('auth.enterRoom'))
    else:
        the_players = players['players']
    return render_template('Inside_the_room/gameRoom.html', players=the_players, game=session['game_name'])

@bp.route('payment', methods=['GET', 'POST'])
@room_required
def payment():
    if request.method == 'POST':
        # Handle payment logic here
        pass
    return render_template('Inside_the_room/payment.html')