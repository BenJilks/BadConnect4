from flask import Flask, render_template, request
from game import *
app = Flask(__name__)
game_manager = GameManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/join', methods=['POST'])
def join():
    data = request.form
    player = request.remote_addr
    name = data['name']
    lobby_name = data['lobby']
    lobby = game_manager.join_lobby(lobby_name, [player, name])
    return render_template('lobby.html', lobby=lobby_name)

if __name__ == '__main__':
    app.run()
