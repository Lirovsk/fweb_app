from app.Models import GameRoom
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

def create_uri(room_name)-> str:
    """Create a new URI for game room"""
    return f"sqlite:///Rooms/{room_name}.db"

def create_game_room(room_name: str):
    """Create a new game room"""
    uri = create_uri(room_name)
    engine = create_engine(uri)
    GameRoom.__table__.create(engine)
    return None

def creating_user(user_name: str, pin:str, room_name: str):
    uri = create_uri(room_name)
    engine = create_engine(uri)
    try: 
        with Session(engine) as session:
            new_user = GameRoom(user_name=user_name, pin=pin, balance=1000)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user
    except Exception as e:
        msg = (f"Error creating user: {e}")
        return msg
    
      # Example usage to create a user in the room