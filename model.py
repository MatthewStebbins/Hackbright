""" Models for the Siren database"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ********************************************************
# ************** Database Table definitions **************

class Room(db.Model):

    __tablename__ = 'rooms'

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'),
                     nullable=False,
                     unique=True)
    created_at = db.Column(db.DateTime,
                           nullable=False)
    
    users = db.relationship('User', back_populates='rooms')
    games = db.relationship('Game', back_populates='rooms')

    def __repr__(self):
        return f'<Room id={self.id}, game_id={self.game_id}, created_at={self.created_at}>'

class Game(db.Model):
    
    __tablename__ = 'games'

    id = db.Column(db.Integer,
                autoincrement=True,
                primary_key=True)
    adventurer_id = db.Column(db.Integer, db.ForeignKey('adventurers.id'),
                     nullable=False,
                     unique=True)
    draw_deck_num = db.Column(db.Integer,
                             db.ForeignKey('decks.deck'),
                             nullable=False)
    ship_deck_num = db.Column(db.Integer,
                             db.ForeignKey('decks.deck'),
                             nullable=False)
    
    rooms = db.relationship('Room', back_populates='games')
    adventurers = db.relationship('Adventurer', back_populates='games')
    decks = db.relationship('Deck', back_populates='games')    

    def __repr__(self):
        return f'Game id={self.id}, aventurer_id={self.adventurer_id}>'


class Adventurer(db.model):

    __tablename__ = 'adventurers'

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    name = db.Column(db.String(12),
                     nullable=False,
                     unique=True) # the name of the adventurer
    picture = db.Column(db.String, nullable=False)  # path to the .png of the adventurer
    health = db.Column(db.Integer, nullable=False)  # base health 
    deck_to_use = db.Column(db.Integer,             # which deck to use for the adventurer
                            db.ForeignKey('decks.deck'),
                            nullable=False) 

    games = db.relationship('Game', back_populates='adventurers')
    equipments = db.relationship('Equipment', back_papulates='adventurers')
    decks = db.relationship('Deck', back_populates='adventurers')

    def __repr__(self):
        return f'<Adventurer id={self.id}, name={self.name}, health={self.health}>'

class Equipment(db.Model):

    __tablename__ = 'equipments'

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True)
    name = db.Column(db.String(12), nullable=False)
    adventurer_id = db.Column(db.Integer,
                              db.ForeignKey('adventurers.id'),
                              nullable=False)
    discription = db.Column(db.String, nullable=False)

    adventurers = db.relationship('Adeventurer', back_populates='equipments')

    def __repr__(self):
        return f'<Equipment id={self.id}, name={self.name}>'

class Deck(db.Model):

    __tablename__ = 'decks'

    id = db.Column(db.Integer,
                autoincrement=True,
                primary_key=True)
    deck = db.Column(db.Integer,
                     nullable=False)
    enemy_id = db.Column(db.Integer,
                         db.ForeignKey('enemies.id'),
                         nullable=False)
    per_deck = db.Column(db.Integer, nullable=False)

    adventurers = db.relationship('Adventurer', back_populates='decks')
    enemies = db.relationship('Enemy', back_populates='decks')

    def __repr__(self):
        return f'<Deck id={self.id}, deck={self.deck}, per_deck={self.per_deck}>'
    
class Enemy(db.Model):

    __tablename__ = 'enemies'

    id = db.Column(db.Integer,
                autoincrement=True,
                primary_key=True)
    name = db.Column(db.String(12),
                     nullable=False,
                     unqiue=True)
    strength = db.Column(db.Integer, nullable=False)

    decks = db.relationship('Deck', back_populates='enemies')

    def __repr__(self):
        return f'<Enemy id={self.id}, name={self.name}, strength={self.strength}'
    
class Equipment_defeats_enemy(db.Model):

    __tablename__ = 'equipment_defeats_enemies'

    enemy_id = db.Column(db.Integer, 
                         db.ForeignKey('enemies.id'),
                         primary_key=True,
                         nullable=False)
    equipment_id = db.Column(db.Integer,
                             db.ForeignKey('equipments.id'),
                             primary_key=True,
                             nullable=False)
    
    enemies = db.relationship('Enemy', back_populates='equipment_defeats_enemies')   
    equipments = db.relationship('Equipment', back_papulates='equipment_defeats_enemies')     
    
    def __repr__(self):
        return f'<Equipment_defeats_enemy enemy id={self.enemy_id}, equipment id={self.equipment_id}>'



# ****************************************
# ********* Connect to Database **********

def connect_to_db(flask_app, db_uri="postgresql:///theSiren", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=True) if your program needs
    # more robust output; this will tell SQLAlchemy to print out
    # every query it executes.

    connect_to_db(app)
