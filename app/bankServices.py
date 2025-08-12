from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from .Models import GameRoom
from .paths import ROOM_PATH
from .Engines.GeneralServices import retrieving_players, retrieving_one_player
from flask import flash, redirect, url_for

class payment:


    def user_to_user(user_from, user_to, amount, game_name):
        atual_room = f"sqlite:///{ROOM_PATH}\{game_name}.db"
        engine = create_engine(atual_room)
        with Session(engine) as session:
            amount = float(amount)
            user_loosing = session.query(GameRoom).filter(GameRoom.user_name == user_from).first()
            user_winning = session.query(GameRoom).filter(GameRoom.user_name == user_to).first()
            if user_loosing.balance >= amount:
                user_loosing.balance -= amount
                user_winning.balance += amount
                session.commit()
                return user_loosing.balance
            else:
                raise ValueError("Insufficient balance for the transaction.")
            return False


    def give_money(user, game_name):
        atual_room = f"sqlite:///{ROOM_PATH}\{game_name}.db"
        engine = create_engine(atual_room)
        with Session(engine) as session:
            try:
                result_player = session.query(GameRoom).filter(GameRoom.user_name == user).first()
            
            except Exception as e:
                flash(str(e))
                print(f"Error retrieving player {user}: {e}")
                return redirect(url_for('room.gameRoom'))
            
            finally:
                result_player.balance += 200
                player_balance = result_player.balance
                session.commit()

        return player_balance