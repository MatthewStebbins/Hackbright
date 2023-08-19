from model import db, Room, Game, User, role, connect_to_db

##################################################
# This file is to hanndle the crud action on the #
# database that is modeled in model.py           #
##################################################


########## Room ############

def create_room(image):
    game = create_game(image)
    db.session.add(game)
    db.session.commit()
    return Room(game_id=game.id)

def get_room_by_id(id):
    # print(id)
    return Room.query.get(id)

########## Game #############

def create_game(image):
    return Game(image=image)

########## User #############

def create_user(room_id, role=role.Player):
    return User(room_id=room_id, role=role)

def get_user_by_id(id):
    return User.query.get(id)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)