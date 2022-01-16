import os
from flask import Flask
from threading import Thread


app = Flask(__name__)

@app.route('/')
def home():
    return '''<a style='text-decoration: none; color: green;' href='https://discord.io/OpenSourceGames'><button">DISCORD SERVER</button></a>'''

def run():
  app.run(host='0.0.0.0',port=3000)

def keep_alive():
    t = Thread(target=run)
    t.start()