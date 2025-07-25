from .Models import GameRoom
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .RoomCreation import create_uri

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