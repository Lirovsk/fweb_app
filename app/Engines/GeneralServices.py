from app.Models import EngineStorage, GameRoom, Base
from .RoomCreation import create_uri
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
from .EngineCreation import engine_for_storage


def retrieving_players (room_name: str):
    """Retrieve all players in a game room."""
    uri = create_uri(room_name)
    engine = create_engine(uri)
    try:
        with Session(engine) as session:
            players = session.query(GameRoom).all()
            return {'trial': True, 'players': players}
    except Exception as e:
        msg = (f"Error retrieving players: {e}")
        return {'trial': False, 'message': msg}

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
    
def insp_default_storage():
    """Inspect the default storage engine."""
    
    try:
        insp = inspect(engine_for_storage)
        return {"trial": True, "tables": insp.get_table_names()}
    except Exception as e:
        msg = (f"Error inspecting default storage: {e}")
        return {"trial": False, "message": msg}
    
def create_default_storage():
    """Create the default storage engine."""
    EngineStorage.__table__.create(engine_for_storage)
    return None

def check_existing(**kwargs):
    """Check if the given parameters exists and return false if one of them is not present."""
    for key, value in kwargs.items():
        if not value:
            return {"trial": False, "message": f"Missing parameter: {key}"}
    return {"trial": True}