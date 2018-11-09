from flask import Flask, render_template, request
from game import *
from connect4 import *
import json
app = Flask(__name__)
game_manager = GameManager()

@app.route('/')
def index():
    player = request.remote_addr
    print('New player: ' + player)
    return render_template('index.html')

@app.route('/join', methods=['POST', 'GET'])
def join():
    player = request.remote_addr
    if request.method == 'POST':
        data = request.form
        name = data['name']
        lobby_name = data['lobby']
        game_manager.register_player(player, name)
        game_manager.join_lobby(lobby_name, player)
    elif request.method == 'GET':
        game = game_manager.get_game(player)
        lobby_name = game.get_name()
    
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
    return 'false'

@app.route('/start_game/<width>/<height>/<connect>')
def start_game(width, height, connect):
    width = int(width)
    height = int(height)
    connect = int(connect)
    player = request.remote_addr
    lobby = game_manager.get_game(player)
    if lobby != None:
        if not lobby.has_started():
            board = Board(lobby.get_players(), width, height, connect)
            lobby.start_game(board)
        return "true"
    return "false"

@app.route('/game')
def game():
    player = request.remote_addr
    game = game_manager.get_game(player)
    if game == None:
        return "You're not in a game!"
    
    board = game.get_game()
    colour = board.player_colour(player)
    return render_template('game.html', colour=colour, 
        width=board.get_width(), height=board.get_height())

@app.route('/place/<x>')
def place(x):
    player = request.remote_addr
    game = game_manager.get_game(player)
    if game != None:
        board = game.get_game()
        if game.is_turn(player):
            if board.place(int(x), player):
                game.next_turn()
                return "true"
    return "false"

@app.route('/curr_turn')
def curr_turn():
    player = request.remote_addr
    game = game_manager.get_game(player)
    if game != None:
        if (game.is_turn(player)):
            turn_text = "your turn:"
        else:
            turn_text = game_manager.player_name(game.curr_player()) + "'s turn:"
        
        baord = game.get_game()
        board_data = baord.get_data()
        has_won = baord.has_won()
        if has_won != None:
            if has_won == player:
                has_won = "you"
            else:
                has_won = game_manager.player_name(has_won)
            game.end_game()

        return json.dumps({'turn_text': turn_text, 'data': board_data, 
            'has_won': has_won})
    return "false"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')
