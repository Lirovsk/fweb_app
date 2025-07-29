"""This file contains functions to create engines"""

from ...app.Models import EngineStorage
from ...app.Models import GameRoom
from ...app.Models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


engine_for_storage = create_engine('sqlite:///engine_storage.db')
#EngineStorage.__table__.create(engine_for_storage)

def create_engine(room_name: str, pin: str, engine_type = "sqlite") -> EngineStorage:
    """Create a new engine storage entry."""
    with Session(engine_for_storage) as session:
        new_engine = EngineStorage(room_name=room_name, pin=pin, engine=engine_type)
        session.add(new_engine)
        session.commit()
        session.refresh(new_engine)  # Refresh to get the ID and other defaults
        return new_engine
    
def delete_engine() -> None:
    """Delete an room if its not in use."""
    with Session(engine_for_storage) as session:
        results =session.query(EngineStorage).all()
        for engine in results:
            if (engine.last_update - datetime.now()) < timedelta(minutes=40):
                room_name = engine.room_name
                session.delete(engine) 
        session.commit()
        
def retrieve_engine(room_name: str) -> EngineStorage:
    """Retrieve an engine storage entry by room name."""
    try:
        with Session(engine_for_storage) as session:
            engine = session.query(EngineStorage).filter_by(room_name=room_name).first()
            return engine
    except Exception as e:
        msg = (f"Error retrieving engine: {e}")
        return msg
    
def delete_room(room_name: str) -> None:
    """Delete a game room."""
    uri = f"sqlite:///Rooms/{room_name}.db"
    try:
        engine = create_engine(uri)
        GameRoom.__table__.drop(engine)
        print(f"Game room '{room_name}' deleted successfully.")
    except Exception as e:
        msg = (f"Error deleting game room: {e}")
        return msg