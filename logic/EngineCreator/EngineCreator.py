from Exceptions import CancelByUser
from app import EngineStorage
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime

class Engine_Storage:
    def __init__(self):
        self.name = "AllEngines"
        self.engine = "sqlite"
        
        

class EngineCreator:
    def __init__(self, name, type):
        self.engine_name = name
        self.engine_type = type
    
    
    @staticmethod
    def get_name():
        pass
    
        
    @classmethod
    def create_engine(cls, name, type):
        new_engine = cls(name, type)
        return new_engine


    def add_engine(self):
        storage = EngineStorage()
        engine = create_engine(f"sqlite:///{storage.name}.db")
        time_now = datetime.now()
        engine_to_add = EngineStorage(
            name=storage.name,
            engine=storage.engine,
            last_update=time_now
        )
        with Session(engine) as session:
            session.add(engine_to_add)
            session.commit()
