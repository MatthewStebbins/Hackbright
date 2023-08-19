"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb theSiren")
os.system('createdb theSiren')

model.connect_to_db(server.app)
with server.app.app_context():
    model.db.create_all()

# with server.app.app_context():
#     model.db.session.add(room)
#     model.db.session.commit()