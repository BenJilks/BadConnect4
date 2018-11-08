from flask import Flask, render_template, request
from game import *
import json
app = Flask(__name__)
game_manager = GameManager()

@app.route('/')
def index():
    player = request.remote_addr
    print('New player: ' + player)
    return render_template('index.html')

@app.route('/join', methods=['POST'])
def join():
    data = request.form
    player = request.remote_addr
    name = data['name']
    lobby_name = data['lobby']
    game_manager.register_player(player, name)
    game_manager.join_lobby(lobby_name, player)
    return render_template('lobby.html', lobby=lobby_name)

@app.route('/lobby_info')
def lobby_info():
    player = request.remote_addr
    lobby = game_manager.get_game(player)
    if lobby != None:
        players = lobby.get_players()
        has_started = lobby.has_started()

        names = []
        for player in players:
            names.append(game_manager.player_name(player))
        return json.dumps({'players': names, 'started': has_started})
    return '404'

@app.route('/start_game')
def start_game():
    player = request.remote_addr
    lobby = game_manager.get_game(player)
    if lobby != None:
        lobby.start_game()

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/place/<x>')
def place(x):
    player = request.remote_addr
    game = game_manager.get_game(player)
    if game != None:
        if game.is_turn(player):    
            game.next_turn(x)
            return "true"
    
    return "false"

@app.route('/curr_turn')
def curr_turn():
    player = request.remote_addr
    game = game_manager.get_game(player)
    if game != None:
        is_turn = game.is_turn(player)
        last_turn = game.played_turn()
        return json.dumps({'is_turn': is_turn, 'last_turn': last_turn})
    return "false"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')
