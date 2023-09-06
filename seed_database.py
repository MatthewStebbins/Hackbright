"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

# EQUIPMENT = {
#     '0':"Defeat the Hive Mother",
#     '1':"Defeat Aliens with strength 3 or loss",
#     '2':"Defeat Aliens with even-numbered strength",
#     '3':"Health: +5",
#     '4':"Health: +3",
#     '5':"Defeat one Alien before exploring the Ship"
# }

os.system("dropdb theSiren -f")
os.system('createdb theSiren')

# model.connect_to_db(server.app)
with server.app.app_context():
    model.db.create_all()

######## Seed adventurers ########
adventurer = crud.create_adventurer('Gunner', 3)

with server.app.app_context():
    model.db.session.add(adventurer)
    model.db.session.commit()

######## Seed equipments #########
with open('data/equipment.json') as f:
    equipment_data = json.loads(f.read())

equipment_list = []
for item in equipment_data:
    
    temp = crud.create_equipment(item['name'],
                                    item['adventurer_id'],
                                    item['discription'], 
                                    item['hp'])
    equipment_list.append(temp)

with server.app.app_context():
    model.db.session.add_all(equipment_list)
    model.db.session.commit()

########## Seed enemies ###########

with open('data/enemy.json') as f:
    enemy_data = json.loads(f.read())

enemy_list = []
for item in enemy_data:
    temp = crud.create_enemy(item['name'], item['strength'])
    enemy_list.append(temp)

with server.app.app_context():
    model.db.session.add_all(enemy_list)
    model.db.session.commit()

######## Seed equipment/enemy iteractions #######

with open('data/equipment-enemy.json') as f:
    equip_enemy_data = json.loads(f.read())

equip_enemy_list = []
for item in equip_enemy_data:
    temp = crud.create_equipment_enemy(item['equipment'], item['enemy'])
    equip_enemy_list.append(temp)

with server.app.app_context():
    model.db.session.add_all(equip_enemy_list)
    model.db.session.commit()
