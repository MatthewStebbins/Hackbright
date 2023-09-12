import requests
from random import choice, randint
from flask import Flask, render_template, request, redirect, jsonify, session
from model import connect_to_db, db, role, deck_type
import crud
import time

URL = "https://api.jikan.moe/v4/characters?page="

app = Flask(__name__)
app.secret_key = "dev"

current_rooms = [12345, 54321, 11111]

EQUIPMENT = {
    '0':"Defeat the Hive Mother",
    '1':"Defeat Aliens with strength 3 or loss",
    '2':"Defeat Aliens with even-numbered strength",
    '3':"Health: +5",
    '4':"Health: +3",
    '5':"Defeat one Alien before exploring the Ship"
}


@app.route('/')
def main():
    return render_template('main.html')

@app.route("/rules")
def rules():
    return render_template('rules.html')

@app.route("/create-room", methods={'POST'})
def create_room():
    user_id = session.get('user')
    image = get_adventurer_image()

    room = crud.create_room(image)
    db.session.add(room)
    db.session.commit()
    user = check_user(user_id, room.id, role.Host)
    room.games.active_user = user_id
    db.session.add(room)
    db.session.commit()    
    session['room'] = room.id

    # print(f'redirecting... to /room/{room.id}')
    payload = jsonify({'status':'success', 'roomcode':room.id})
    # print(payload.response)
    return payload

@app.route("/join-room")
def join_room():
    roomcode = request.args['room']
    # print(roomcode)

    if crud.get_room_by_id(roomcode):
        return jsonify({"status":"active", "roomcode":roomcode})
    else:
        return jsonify({"status":"inactive", "roomcode":roomcode})
    
@app.route("/room/<roomcode>", methods={'POST', 'GET'})
def game_room(roomcode):
    # print(f'in /room/{roomcode}')
    user_id = session.get('user')
    # print(user_id)
    room = crud.get_room_by_id(roomcode)
    user = check_user(user_id, room.id)
    session['room'] = room.id

    if room:
        return render_template('game.html')
        # return render_template('gameroom.html', roomcode=roomcode, image=room.games.image, crew=room.games.adventurers.name)   
    else:
        print('redirecting to /')
        return redirect('/')

@app.route('/todo')
def todo():
    return render_template('todo.html')

@app.route('/test')
def test():
    state = win_loss(1, 1)
    print(state)
    if state == '':
        return redirect('/rules')
    return state
    #return render_template('todo.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/win')
def win():
    return render_template('win.html')

@app.route('/loss')
def loss():
    return render_template('loss.html')


############################################
#              API functions               #
############################################  

@app.route('/api/load_room')
def load_room():
    room_id = session.get('room')
    room = crud.get_room_by_id(room_id)
    # print(room)

    advent_id = room.games.adventurers.id
    # print(advent_id)

    equipment = crud.get_equipment_by_adventurer_id_all(advent_id)

    return jsonify(image=room.games.image,
                    crew=room.games.adventurers.name,
                    equipment=equipment,
                    activeUser=room.games.active_user,
                    currentUser=session.get('user'))

@app.route('/api/draw_card')
def draw_card():
    room_id = session.get('room')
    room = crud.get_room_by_id(room_id)

    game_id = room.game_id
    card = crud.get_random_card(game_id, deck_type.Draw)
    crud.remove_card(card.game_id, card.enemy_id, deck_type.Draw)
    print(card.enemies)
    return jsonify(image='/static/img/Enemies/test.png',
                    name=card.enemies.name,
                    strength=card.enemies.strength)

@app.route('/api/pass')
def passTurn():
    user_id = session.get('user')
    room_id = session.get('room')
    # print(user_id)


    success = crud.set_user_passed(user_id)
    (active_user, ship_phase) = crud.get_next_active_user(user_id, room_id)

    return jsonify(success=success, activeUser=active_user, shipPhase=ship_phase)

@app.route('/api/add/<name>', methods={'POST', 'GET'})
def addCard(name):
    user_id = session.get('user')
    room_id = session.get('room')
    room = crud.get_room_by_id(room_id)
    enemy_id = crud.get_enemy_id_by_name(name)

    game_id = room.game_id
    print(game_id)
    print(enemy_id)

    success = crud.add_card(game_id, enemy_id, deck_type.Ship)
    (active_user, ship_phase) = crud.get_next_active_user(user_id, room_id)

    return jsonify(success=success, activeUser=active_user)

@app.route('/api/discard_equipment/<equipment_name>')
def discardEquipment(equipment_name):
    equipment_id = crud.get_equipment_by_name(equipment_name)
    user_id = session.get('user')
    room_id = session.get('room')
    room = crud.get_room_by_id(room_id)

    game_id = room.game_id

    success = crud.discard_equipment(game_id, equipment_id)
    active_user = crud.get_next_active_user(user_id, room_id)

    return jsonify(success=success, equipment_id=equipment_id, activeUser=active_user)

@app.route('/api/ship/start')
def startship():
    room_id = session.get('room')
    room = crud.get_room_by_id(room_id)
    game_id = room.game_id

    card = crud.get_random_card(game_id, deck_type.Ship)
    # crud.remove_card(game_id, card.enemy_id, deck_type.Ship)

    effective_active_equipment = crud.get_active_equipment_by_enemy_id(game_id, card.enemies.id)
    print(effective_active_equipment)
    hp = crud.get_total_hp(room)
    return jsonify(image='/static/img/Enemies/test.png',
                    name=card.enemies.name,
                    strength=card.enemies.strength,
                    hp=hp,
                    equipment=effective_active_equipment)

@app.route('/api/ship/combat')
def combat():
    room_id = session.get('room')
    room = crud.get_room_by_id(room_id)
    game_id = room.game_id
    equipment_id = request.args.get('equipment')
    enemy_name = request.args.get('enemy')
    damage = request.args.get('damage')
    print('equipment: ', equipment_id)
    print('damage: ', damage)

    # Handle previous card
    crud.take_damage(game_id, damage)
    if equipment_id == 6:
        enemy_id = crud.get_enemy_id_by_name(enemy_name)
        termial_detonator(game_id, enemy_id)

    # Check if game is over

    hp = crud.get_total_hp(room)
    state = win_loss(hp)
    if state != '':
        return state
    
    # If game is not over load next enemy

    card = crud.get_random_card(game_id, deck_type.Ship)
    crud.remove_card(game_id, card.enemy_id, deck_type.Ship)

    effective_active_equipment = crud.get_active_equipment_by_enemy_id(game_id, card.enemies.id)

    return jsonify(image='/static/img/Enemies/test.png',
                    name=card.enemies.name,
                    strength=card.enemies.strength,
                    hp=hp,
                    equipment=effective_active_equipment)


############################################
#           Helper functions               #
############################################

def check_user(user_id, room_id, role=role.Player):
    user = crud.get_user_by_id(user_id)

    if user:
        if user.room_id != room_id:
            user.room_id = room_id
            user.user_passed = False
            db.session.add(user)
            db.session.commit()
        return user
    else:
        user = crud.create_user(room_id, role)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.id
        return user

def get_adventurer_image():

    bad_url = 'https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png'
    image = bad_url

    while image == bad_url:
        print('bad url if twice in a row')
        randnum = randint(1,1000)
        res = requests.get(URL+ str(randnum))
        results = res.json()
        image = results['data'][2]['images']['jpg']['image_url']

    return image    

def termial_detonator(game_id, enemy_id):
    crud.remove_card_all(game_id, enemy_id, deck_type.Ship)
    crud.discard_equipment(game_id, 6)

def win_loss(hp, game_id):
    state = ''
    print('HP: ',hp)
    print('game_id: ',game_id)
    number_of_cards = crud.cards_in_deck(game_id, deck_type.Ship)
    if hp <= 0:
        state = loss()
    elif number_of_cards <= 0:
        state = win()

    return state

def loss():
    return redirect('/loss')

def win():
    return redirect('/win')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")