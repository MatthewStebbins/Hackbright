from model import db, Room, Game, User, role, deck_type, Adventurer, Equipment, Enemy, Deck, connect_to_db, Equipment_state, Equipment_defeats_enemy
import crud
import json
import server
import model
from sqlalchemy.sql import func
import random

##################################################
# This file is to hanndle the crud action on the #
# database that is modeled in model.py           #
##################################################

model.connect_to_db(server.app)

########## Room ############

def create_room(image, advent_id=1):
    game = create_game(image, advent_id)
    return Room(game_id=game.id)

def get_room_by_id(id):
    # print(id)
    return Room.query.get(id)

########## Game #############

def create_game(image, advent_id=1):
    game = Game(image=image, adventurer_id=advent_id)
    db.session.add(game)
    db.session.commit()
    build_draw_deck(game.id)
    build_starting_states(game.id)
    return game

def set_active_user(user_id, room_id):
    room = Room.query.filter(Room.id == room_id).first()
    room.games.active_user = user_id
    db.session.add(room)
    db.session.commit()    

########## User #############

def create_user(room_id, role=role.Player):
    return User(room_id=room_id, role=role)

def get_user_by_id(id):
    return User.query.get(id)

def set_user_passed(id):
    user = User.query.filter(User.id == id).first()
#    user.user_passed = True
    db.session.add(user)
    db.session.commit()

    return True

def get_next_active_user(user_id, room_id):
    users_in_room_not_passed = db.session.query(User.id).filter(User.room_id == room_id, User.user_passed == False).order_by(User.id).all()
    print(users_in_room_not_passed)
    current_index = users_in_room_not_passed.index((user_id,))
    ship_phase = False
    if len(users_in_room_not_passed) <= 2:
        ship_phase = True

    if current_index + 1 == len(users_in_room_not_passed):
        new_active_user = users_in_room_not_passed[0][0]
    else:
        new_active_user = users_in_room_not_passed[current_index + 1][0]

    set_active_user(new_active_user, room_id)

    return (new_active_user, ship_phase) 

######## Adventurer #########

def create_adventurer(name, health):
    return Adventurer(name=name, health=health)

def get_adventurer_by_name(name):
    return Adventurer.query.filter(Adventurer.name == name).first()

def get_total_hp(room):
    game_id = room.game_id
    advent_id = room.games.advent_id
    
    total_hp = 0
    health = db.session.query(adventurer.health).filter(adventurer.adventurer_id == advent_id).first()
    print('adventurer HP: ' + hp)
    total_hp += health

    active_equipments = get_all_active_equipment(game_id)

    for item in active_equipments:
        hp = item.equipments.hp
        if hp != 0:
            total_hp += hp

    print('Total hp:' + total_hp)

    return total_hp

######### Equipment #########

def create_equipment(name, advent_id, discription, hp):
    return Equipment(name=name, adventurer_id=advent_id, discription=discription, hp=hp)

def get_equipment_by_adventurer_id_all(advent_id):
    temp = Equipment.query.filter(Equipment.adventurer_id == advent_id).all()
    # print(temp)
    temp_list = []
    for u in temp:
        temp_list.append({'name':u.name, 'discription':u.discription, 'adventurer_id':u.adventurer_id})    
    # print(temp_list)
    return temp_list

def get_equipment_by_name(name):
    equipment = Equipment.query.filter(Equipment.name == name).first()
    return equipment.id

########### Enemy ###########

def create_enemy(name, strength):
    return Enemy(name=name, strength=strength)

def get_enemy_id_by_name(name):
    enemy = db.session.query(Enemy.id).filter(Enemy.name == name).first()
    return enemy[0]

########### Deck ############

def create_deck(game_id, enemy_id, per_deck, deck_type):
    return Deck(game_id=game_id, enemy_id=enemy_id, in_deck=per_deck, deck_type=deck_type)

def build_draw_deck(game_id):
    with open('data/deck.json') as f:
        deck_data = json.loads(f.read())

    deck_list = []
    for item in deck_data:
        temp = crud.create_deck(game_id, item['enemy_id'], item['per_deck'], deck_type=deck_type.Draw)
        deck_list.append(temp)

    with server.app.app_context():
        db.session.add_all(deck_list)
        db.session.commit()

def get_random_card(game_id, d_type):
    cards = Deck.query.filter(Deck.game_id == game_id, Deck.deck_type == d_type ).all()
    print(cards)

    if len(cards) >= 1:
        weights = []
        for card in cards:
            weights.append(card.in_deck)
        print(weights)
        card = random.choices(cards, weights=weights)
        card = card[0]
    else:
        card = -1
    print(card)
    return card

def remove_card(game_id, enemy_id, deck_type):
    card = Deck.query.filter(Deck.game_id == game_id,
                            Deck.enemy_id == enemy_id,
                             Deck.deck_type == deck_type).first()
    
    if card.in_deck <= 1:
        db.session.delete(card)
    else:
        card.in_deck -= 1
    db.session.commit()

def add_card(game_id, enemy_id, deck_type):
    card = Deck.query.filter(Deck.game_id == game_id,
                            Deck.enemy_id == enemy_id,
                             Deck.deck_type == deck_type).first()
    
    if card == None:
        card = crud.create_deck(game_id, enemy_id, 1, deck_type=deck_type.Ship)        
        db.session.add(card)
    else:
        card.in_deck += 1
    db.session.commit()    

    return True

########## Equipment_state ###########

def create_equipment_state(game_id, equipment_id):
    return Equipment_state(game_id=game_id, equipment_id=equipment_id)

def build_starting_states(game_id):
    equipments = Equipment.query.all()

    states_list = []
    for item in equipments:
        
        temp = crud.create_equipment_state(game_id, item.id)
        states_list.append(temp)

    with server.app.app_context():
        db.session.add_all(states_list)
        db.session.commit()

def discard_equipment(game_id, equipment_id):
    state = Equipment_state.query.filter(Equipment_state.game_id == game_id, 
                                        Equipment_state.equipment_id == equipment_id).first()
    state.state = False

    db.session.add(state)
    db.session.commit()

    return True

def get_all_active_equipment(game_id):
    return Equipment_state.query.filter(Equipment_state.game_id == game_id, Equipment_state.state == True).all()

########## Equipment\enemy interactions ###########

def create_equipment_enemy(equip_id, enemy_id):
    return Equipment_defeats_enemy(equipment_id=equip_id, enemy_id=enemy_id)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)