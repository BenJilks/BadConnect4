from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit
from game import GameManager
from connect4 import Board
import json
app = Flask(__name__)
socketio = SocketIO(app)
game_manager = GameManager()

html_escape_table = {
    "&": "&amp;",
    '"': "&#34;",
    "'": "&#39;",
    ">": "&gt;",
    "<": "&lt;",
}

def html_escape(text):
    return "".join(html_escape_table.get(c,c) for c in text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lobby', methods=['POST', 'GET'])
def lobby():
    player = request.remote_addr
    if request.method == 'POST':
        data = request.form
        name = data['name']
        lobby_name = data['lobby']
        game_manager.register_player(player, name)
    elif request.method == 'GET':
        game = game_manager.get_game(player)
        if game == None:
            return "You're not in a lobby!"
        lobby_name = game.get_name()
    
    return render_template('lobby.html', lobby=lobby_name)

@app.route('/game')
def game():
    player = request.remote_addr
    game = game_manager.get_game(player)
    if game == None:
        return "You're not in a game!"
    
    board = game.get_game()
    colour = board.player_colour(player)
    name = game_manager.player_name(player)
    return render_template('game.html', 
        colour=colour, 
        width=board.get_width(), 
        height=board.get_height(), 
        name=name, secure=False)

@socketio.on('join')
def join(lobby_name):
    player = request.remote_addr
    curr_game = game_manager.get_game(player)
    if curr_game != None:
        print('Message:', player, 'leaving', curr_game.get_name())
        game_manager.leave_lobby(player)
        update_players(curr_game)
        leave_room(curr_game.get_name())
    
    print('Message:', player, 'joining', lobby_name)
    lobby = game_manager.join_lobby(lobby_name, player)
    join_room(lobby_name)
    update_players(lobby)

@socketio.on('start_game')
def start_game(width, height, connect):
    player = request.remote_addr
    lobby = game_manager.get_game(player)

    width = int(width)
    height = int(height)
    connect = int(connect)
    if not lobby.has_started():
        print('starting game', lobby.get_name())
        board = Board(lobby.get_players(), width, height, connect)
        lobby.start_game(board)
        emit('goto_game', room=lobby.get_name())

@socketio.on('game_started')
def game_started():
    player = request.remote_addr
    game = game_manager.get_game(player)
    join_room(game.get_name())
    send_board_update(game, player)

@socketio.on('place')
def place(id):
    player = request.remote_addr
    game = game_manager.get_game(player)

    if game.is_turn(player):
        id = int(id)
        board = game.get_game()
        if board.place(id, player):
            game.next_turn()
            board.check_won()
            send_board_update(game, player)
            print('Message:', player, 'placed', id)

def send_board_update(game, player):
    board = game.get_game()
    turn = game.curr_player()
    turn_text = html_escape(game_manager.player_name(turn)) + '\'s turn'

    has_won = board.has_won()
    if has_won != None:
        has_won = game_manager.player_name(has_won)
    data = {'data': board.get_data(), 'turn_text': turn_text, 'has_won': has_won}
    socketio.send(json.dumps(data), json=True, room=game.get_name())

def create_player_list(lobby):
    player_list = ''
    for player in lobby.get_players():
        player_list += html_escape(game_manager.player_name(player)) + '<br>'
    return player_list

def update_players(lobby):
    player_list = create_player_list(lobby)
    socketio.send(player_list, room=lobby.get_name())

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='80')
