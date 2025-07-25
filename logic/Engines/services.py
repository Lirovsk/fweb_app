from .Models import EngineStorage, GameRoom, Base
from .RoomCreation import create_uri
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def retrieving_players (room_name: str):
    """Retrieve all players in a game room."""
    uri = create_uri(room_name)
    engine = create_engine(uri)
    try:
        with Session(engine) as session:
            players = session.query(GameRoom).all()
            return players
    except Exception as e:
        msg = (f"Error retrieving players: {e}")
        return msg
    
def retrieving_one_player(room_name: str, user_name: str):
    """Retrieve a specific player in a game room."""
    uri = create_uri(room_name)
    engine = create_engine(uri)
    try:
        with Session(engine) as session:
            player = session.query(GameRoom).filter_by(user_name=user_name).first()
            return player
    except Exception as e:
        msg = (f"Error retrieving player {user_name}: {e}")
        return msg