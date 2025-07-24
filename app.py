from flask import Flask, url_for, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from logic.game_db import generate_db_path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///engine_storage.db'
db = SQLAlchemy(app)

class EngineStorage(db.Model):
    __tablename__ = 'engine_storage'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    engine = db.Column(db.String(50), nullable=False)
    last_update = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Engine {self.name}  last updated at {self.last_update}>'


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_engines', methods=['GET'])
def create_engines():
    return render_template('create_gameRoom.html')

@app.route('/engines', methods=['POST'])
def create_game():
    name = request.form['name'] # Changed from 'Name of the game'

    new_game = EngineStorage(name=name, engine="sqlite", last_update=datetime.now())
    db.session.add(new_game)
    db.session.commit()
    return redirect(url_for('enterRoom', name=name))

@app.route('/engines/<name>')
def enterRoom(name):
    from logic.game_db import generate_db_path, game_Db
    db_path = generate_db_path(name)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    with app.app_context():
        game_Db.__table__.create(db.engine, checkfirst=True)
    return render_template('enter_game.html', name=name)

@app.route('/engines/<name>/<user>', methods=['POST'])
def enter_game(name, user):
    from logic.game_db import game_Db
    db_path = generate_db_path(name)
    with app.app_context():
        user = request.form['user']
        new_user = game_Db(name=user, balance=0.0)
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('view_engine', id=new_user.id))
    