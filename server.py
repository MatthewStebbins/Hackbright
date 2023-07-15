import requests

from random import choice, randint
from flask import Flask, render_template, request

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
    return render_template('todo.html')

@app.route("/join-room")
def join_room():
    return render_template('todo.html')

if __name__ == '__main__':

    app.run(debug=True, host="0.0.0.0")