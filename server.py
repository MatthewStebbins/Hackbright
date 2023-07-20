import requests
from random import choice, randint
from flask import Flask, render_template, request, redirect, jsonify

URL = "https://api.jikan.moe/v4/characters?page="

app = Flask(__name__)

current_rooms = [12345, 54321, 11111]

@app.route('/')
def main():
    return render_template('main.html')

@app.route("/rules")
def rules():
    return render_template('rules.html')

@app.route("/create-room")
def create_room():

    return jsonify({"status":"success"})

@app.route("/join-room")
def join_room():
    roomcode = request.args['room']
    print(roomcode)
    if int(roomcode) in current_rooms:
        return jsonify({"status":"active", "roomcode":roomcode})
    else:
        return jsonify({"status":"inactive", "roomcode":roomcode})
    
@app.route("/room/<roomcode>")
def game_room(roomcode):
    if not(int(roomcode) in current_rooms):
        return redirect('/')
    else:
        randnum = randint(1,1000)
        res = requests.get(URL+ str(randnum))
        results = res.json()
        image = results['data'][2]['images']['jpg']['image_url']
        return render_template('gameroom.html', roomcode=roomcode, image=image, crew='Gunner')

@app.route('/todo')
def todo():
    return render_template('todo.html')

if __name__ == '__main__':

    app.run(debug=True, host="0.0.0.0")