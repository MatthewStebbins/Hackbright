import requests
from random import choice, randint
from flask import Flask, render_template, request, redirect, jsonify, session
from model import connect_to_db, db, role
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
    
    image = get_adventurer_image()

    room = crud.create_room(image)
    db.session.add(room)
    db.session.commit()

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
    
@app.route("/room/<roomcode>", methods={'POST'})
def game_room(roomcode):
    # print(f'in /room/{roomcode}')
    user_id = session.get('user')
    print(user_id)
    room = crud.get_room_by_id(roomcode)
    user = check_user(user_id, room.id)

    if room:
        return render_template('gameroom.html', roomcode=roomcode, image=room.games.image, crew='Gunner')   
    else:
        print('redirecting to /')
        return redirect('/')

@app.route('/todo')
def todo():
    return render_template('todo.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/api/load_room')
def api_portrait():
    randnum = randint(1,1000)
    res = requests.get(URL+ str(randnum))
    results = res.json()
    image = results['data'][2]['images']['jpg']['image_url']
    print(image)
    return jsonify(image=image, crew='Gunner', equipment=EQUIPMENT)

############################################
#           Helper functions               #
############################################

def check_user(user_id, room_id, role=role.Player):
    user = crud.get_user_by_id(user_id)

    if user:
        if user.room_id != room_id:
            user.room_id = room_id
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

    randnum = randint(1,1000)
    res = requests.get(URL+ str(randnum))
    results = res.json()
    image = results['data'][2]['images']['jpg']['image_url']

    return image    

if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")