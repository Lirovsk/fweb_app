"""This file contains functions to create engines"""

from Models import EngineStorage
from Models import GameRoom
from Models import Base
from sqlalchemy import create_engine


engine = create_engine('sqlite:///engine_storage.db')
Base.metadata.create_all(engine)

