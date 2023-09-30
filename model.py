""" Models for the Siren database"""
import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ********************************************************
# ************ Association Table definitions *************

# equipment_enemy = db.Table('equipment_enemy',
#                         db.Column('equipment_id', db.Integer, db.ForeignKey('equipments.id')),
#                         db.Column('enemy_id', db.Integer, db.ForeignKey('enemies.id')))

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
                            nullable=False, default=db.func.current_timestamp())
    
    users = db.relationship('User', back_populates='rooms')
    games = db.relationship('Game', uselist=False, back_populates='rooms')

    def __repr__(self):
        return f'<Room id={self.id}, Game_id={self.game_id} created_at={self.created_at}>'

class Game(db.Model):
    
    __tablename__ = 'games'

    id = db.Column(db.Integer,
                autoincrement=True,
                primary_key=True)
    image = db.Column(db.String, nullable=False)
    damage = db.Column(db.Integer, nullable=False, default= 0)
    adventurer_id = db.Column(db.Integer, db.ForeignKey('adventurers.id'),
                        nullable=False)
    active_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    started = db.Column(db.Boolean, nullable=False, default=False)
    
    rooms = db.relationship('Room', back_populates='games')
    users = db.relationship('User', back_populates='games')
    adventurers = db.relationship('Adventurer', uselist=False, back_populates='games')
    decks = db.relationship('Deck', back_populates='games')    
    equipment_states = db.relationship('Equipment_state', back_populates='games')

    def __repr__(self):
        return f'Game id={self.id}, aventurer_id={self.adventurer_id}>'

class Adventurer(db.Model):

    __tablename__ = 'adventurers'

    id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    name = db.Column(db.String(12),
                    nullable=False,
                    unique=True) # the name of the adventurer
    # picture = db.Column(db.String, nullable=False)  # path to the .png of the adventurer
    health = db.Column(db.Integer, nullable=False)  # base health 

    games = db.relationship('Game', back_populates='adventurers')
    equipments = db.relationship('Equipment', back_populates='adventurers')
    # decks = db.relationship('Deck', back_populates='adventurers')

    def __repr__(self):
        return f'<Adventurer id={self.id}, name={self.name}, health={self.health}>'

class Equipment(db.Model):

    __tablename__ = 'equipments'

    id = db.Column(db.Integer,
                    autoincrement=True,
                    primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    adventurer_id = db.Column(db.Integer,
                                db.ForeignKey('adventurers.id'),
                                nullable=False)
    discription = db.Column(db.String, nullable=False)
    hp = db.Column(db.Integer, nullable=False)

    adventurers = db.relationship('Adventurer', back_populates='equipments')
    equipment_states = db.relationship('Equipment_state', back_populates='equipments')
    equipment_defeats_enemies = db.relationship('Equipment_defeats_enemy', back_populates='equipments')

    def __repr__(self):
        return f'<Equipment id={self.id}, name={self.name}>'

class Equipment_state(db.Model):

    __tablename__ = 'equipment_states'

    id = db.Column(db.Integer,
                autoincrement=True,
                primary_key=True)
    game_id = db.Column(db.Integer,
                        db.ForeignKey('games.id'),
                        nullable=False)
    equipment_id = db.Column(db.Integer,
                        db.ForeignKey('equipments.id'),
                        nullable=False)
    state = db.Column(db.Boolean, nullable=False, default=True)

    games = db.relationship('Game', back_populates='equipment_states')
    equipments = db.relationship('Equipment', back_populates='equipment_states')

    def __repr__(self):
        return f'<Equipment_state id={self.id}, game id={self.game_id}, equipment id={self.equipment_id}, state={self.state}>'

class deck_type(enum.Enum):
    Ship = 'Ship'
    Draw = 'Draw'

class Deck(db.Model):

    __tablename__ = 'decks'

    id = db.Column(db.Integer,
                autoincrement=True,
                primary_key=True)
    game_id = db.Column(db.Integer,
                        db.ForeignKey('games.id'),
                        nullable=False)
    enemy_id = db.Column(db.Integer,
                            db.ForeignKey('enemies.id'),
                            nullable=False)
    in_deck = db.Column(db.Integer, nullable=False)
    deck_type = db.Column(db.Enum(deck_type), nullable=False)

#     adventurers = db.relationship('Adventurer', back_populates='decks')
    enemies = db.relationship('Enemy', lazy='subquery', uselist=False, back_populates='decks')
    games = db.relationship('Game', back_populates='decks')

    def __repr__(self):
        return f'<Deck id={self.id}, game_id={self.game_id}, enemy_id={self.enemy_id}, in_deck={self.in_deck}>'
    
class Enemy(db.Model):

    __tablename__ = 'enemies'

    id = db.Column(db.Integer,
                autoincrement=True,
                primary_key=True)
    name = db.Column(db.String(20),
                        nullable=False,
                        unique=True)
    strength = db.Column(db.Integer, nullable=False)

    decks = db.relationship('Deck', uselist=False, back_populates='enemies')
    # equipment_defeats_enemies = db.relationship('Enemy', back_populates='enemies')
#     equipments = db.relationship('Equipment',
#                             secondary='Equipment_defeats_enemy',
#                               back_populates='enemies')

    def __repr__(self):
        return f'<Enemy id={self.id}, name={self.name}, strength={self.strength}'
    
class Equipment_defeats_enemy(db.Model):

    __tablename__ = 'equipment_defeats_enemies'

    equipment_id = db.Column(db.Integer,
                                db.ForeignKey('equipments.id'),
                                primary_key=True,
                                nullable=False)    
    enemy_id = db.Column(db.Integer, 
                            db.ForeignKey('enemies.id'),
                            primary_key=True,
                            nullable=False)
    
    equipments = db.relationship('Equipment', back_populates='equipment_defeats_enemies')

    def __repr__(self):
        return f'<Equipment_defeats_enemy enemy id={self.enemy_id}, equipment id={self.equipment_id}>'

class role(enum.Enum):
    Host = 'Host'
    Player = 'Player'

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                autoincrement=True,
                primary_key=True)
    room_id = db.Column(db.Integer,
                        db.ForeignKey('rooms.id'),
                        nullable=False)
    role = db.Column(db.Enum(role), nullable=False)
    user_passed = db.Column(db.Boolean, default=False)

    games = db.relationship('Game', back_populates='users')
    rooms = db.relationship('Room', back_populates='users')
#     users_stats = db.relationship('User_stats', uselist=False, backpopulates='users')

    def __repr__(self):
        return f'<User id={self.id}, room_id={self.room_id}, user_passed={self.user_passed}>'


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
