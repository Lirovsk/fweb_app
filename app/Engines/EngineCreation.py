"""This file contains functions to create engines"""

from app.Models import EngineStorage
from app.Models import GameRoom
from app.Models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime, timedelta


engine_for_storage = create_engine('sqlite:///engine_storage.db')
#EngineStorage.__table__.create(engine_for_storage)
# replace this function with a class, the class should contain different classmethods to create diferent types of games.
def create_engine_data(room_name: str, pin: str, engine_type = "sqlite") -> EngineStorage:
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
        
def retrieve_engine_data(room_name: str) -> list:
    """
    Retrieve an engine storage entry by room name.
    Return -> list;
    format: (bool, engine | msg)
    """
    try:
        with Session(engine_for_storage) as session:
            engine = session.query(EngineStorage).filter_by(room_name=room_name).first()
            return (True, engine)
    except Exception as e:
        msg = (f"Error retrieving engine: {e}")
        return (False, msg)

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
    
class engineConstructor:
    def __init__(self, game_name: str, game_pin: str,last_used: datetime,
                value_for_round: float, bank_needed: bool, engine = "sqlite"):
        self.game_name = game_name
        self.game_pin = game_pin
        self.last_used = last_used
        self.value_for_round = value_for_round
        self.bank_neede = bank_needed
        self.engine = engine


    @classmethod
    def game_type1(cls, game_name_, game_pin_,):
        time = datetime.now()
        value = 300
        return engineConstructor(game_name = game_name_, game_pin = game_pin_, last_used = time, 
                                value_for_round = value, bank_needed= False)


    @classmethod
    def game_type2(cls, game_name_, game_pin_,):
        time = datetime.now()
        value = 300
        return engineConstructor(game_name = game_name_, game_pin = game_pin_, last_used = time, 
                                value_for_round = value, bank_needed= True)   


    @classmethod
    def game_type3(cls, game_name_, game_pin_,):
        time = datetime.now()
        value = 600
        return engineConstructor(game_name = game_name_, game_pin = game_pin_, last_used = time, 
                                value_for_round = value, bank_needed= False) 
    

    @classmethod
    def game_type4(cls, game_name_, game_pin_,):
        time = datetime.now()
        value = 600
        return engineConstructor(game_name = game_name_, game_pin = game_pin_, last_used = time, 
                                value_for_round = value, bank_needed= True)