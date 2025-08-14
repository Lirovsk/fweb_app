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
def create_engine_data(gameType, game_name, game_pin) -> EngineStorage: #erase this method and replace it
    """Create a new engine storage entry."""
    match gameType:
        case 'gameType1':
            constructor = engineConstructor.game_type1
        case 'gameType2':
            constructor = engineConstructor.game_type2
        case 'gameType3':
            constructor = engineConstructor.game_type3
        case 'gameType4':
            constructor = engineConstructor.game_type4

    game_local = constructor(game_name, game_pin)
    new_engine = EngineStorage(
        room_name=game_local.game_name,
        pin=game_local.game_pin,
        engine=game_local.engine,
        value_for_round=game_local.value_for_round,
        bank_needed=game_local.bank_needed,
        initial_value=game_local.initial_value
    )
    
    with Session(engine_for_storage) as session:
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
    def __init__(self, game_name: str, game_pin: str,
                value_for_round: float, bank_needed: bool, initial_value: int, engine = "sqlite"):
        self.game_name = game_name
        self.game_pin = game_pin
        self.value_for_round = value_for_round
        self.bank_needed = bank_needed
        self.initial_value = initial_value
        self.engine = engine
        #last_used does not need to be stored


    @classmethod
    def game_type1(cls, game_name_: str, game_pin_: str):
        time = datetime.now()
        value_for_round_ = 300
        initial_value_ = 1000
        return engineConstructor(game_name=game_name_, game_pin=game_pin_,
                                value_for_round=value_for_round_, bank_needed=False, initial_value=initial_value_)


    @classmethod
    def game_type2(cls, game_name_: str, game_pin_: str):
        time = datetime.now()
        value_for_round_ = 300
        initial_value_ = 1500
        return engineConstructor(game_name=game_name_, game_pin=game_pin_,
                                value_for_round=value_for_round_, bank_needed=True, initial_value=initial_value_)


    @classmethod
    def game_type3(cls, game_name_: str, game_pin_: str):
        time = datetime.now()
        value_for_round_ = 600
        initial_value_ = 2000
        return engineConstructor(game_name=game_name_, game_pin=game_pin_,
                                value_for_round=value_for_round_, bank_needed=False, initial_value=initial_value_)


    @classmethod
    def game_type4(cls, game_name_: str, game_pin_: str):
        time = datetime.now()
        value_for_round_ = 600
        initial_value_ = 2500
        return engineConstructor(game_name=game_name_, game_pin=game_pin_,
                                value_for_round=value_for_round_, bank_needed=True, initial_value=initial_value_)