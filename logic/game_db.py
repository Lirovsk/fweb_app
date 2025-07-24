from app import db
from flask_sqlalchemy import SQLAlchemy


def generate_db_path(name):
    return f"sqlite:///rooms/{name}.sqlite"


class game_Db(db.Model):
    __tablename__ = 'game_db'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Game {self.name}>'

