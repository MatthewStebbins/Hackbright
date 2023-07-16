import requests
from random import choice, randint
from flask import Flask, render_template, request, redirect, jsonify

URL = "https://api.jikan.moe/v4/characters?page="

app = Flask(__name__)


@app.route('/')
def api_call():
    randnum = randint(1,1000)
    res = requests.get(URL+ str(randnum))
    results = res.json()
    image = results['data'][2]['images']['jpg']['image_url']
    name = results['data'][2]['name']
    return render_template('main.html', image=image, name=name)

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
    if roomcode == '12345':
        return jsonify({"status":"active", "roomcode":roomcode})
    else:
        return jsonify({"status":"inactive", "roomcode":roomcode})

@app.route('/todo')
def todo():
    return render_template('todo.html')

if __name__ == '__main__':

    app.run(debug=True, host="0.0.0.0")