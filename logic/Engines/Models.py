from typing import Optional
from sqlalchemy import ( Integer,
                        String,
                        DateTime)
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column)
from datetime import datetime




class Base(DeclarativeBase):
    pass



class EngineStorage(Base):
    __tablename__ = 'engine_storage'

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    room_name : Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    engine : Mapped[str] = mapped_column(String(50), nullable=False)
    pin : Mapped[str] = mapped_column(String(5), nullable=False)
    last_update : Mapped[Optional[DateTime]] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __str__(self):
        return f"EngineStorage (id={self.id}, room_name={self.room_name}, engine={self.engine}, last_update={self.last_update})"



class GameRoom(Base):
    __tablename__ = 'game_room'
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name : Mapped[str] = mapped_column(String(50), nullable=False)
    balance : Mapped[int]
    pin : Mapped[str] = mapped_column(String(4), nullable=False)
    
    def __str__(self):
        return f"GameRoom (id={self.id}, user_name={self.user_name}, balance={self.balance}, pin={self.pin})"
    
