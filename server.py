from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit
from game import GameManager
from connect4 import Connect4Board
from cards import CardStack
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

@app.route('/connect4')
def connect4():
    player = request.remote_addr
    game = game_manager.get_game(player)
    if game == None:
        return "You're not in a game!"
    
    board = game.get_game()
    colour = board.player_colour(player)
    name = game_manager.player_name(player)
    return render_template('connect4.html', 
        colour=colour, 
        width=board.get_width(), 
        height=board.get_height(), 
        name=name, secure=False)

@app.route('/cards')
def cards():
    player = request.remote_addr
    game = game_manager.get_game(player)
    if game == None:
        return "You're not in a game!"    
    return render_template('cards.html', player=player)

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

def create_player_list(lobby):
    player_list = ''
    for player in lobby.get_players():
        player_list += html_escape(game_manager.player_name(player)) + '<br>'
    return player_list

def update_players(lobby):
    player_list = create_player_list(lobby)
    socketio.send(player_list, room=lobby.get_name())

# Connect4

@socketio.on('start_connect4')
def start_connect4(width, height, connect):
    player = request.remote_addr
    lobby = game_manager.get_game(player)

    width = int(width)
    height = int(height)
    connect = int(connect)
    print('starting connect4', lobby.get_name())
    board = Connect4Board(lobby.get_players(), width, height, connect)
    lobby.start_game(board)
    emit('goto_game', '/connect4', room=lobby.get_name())

@socketio.on('game_started_connect4')
def game_started_connect4():
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

# Cards

@socketio.on('start_cards')
def start_cards():
    player = request.remote_addr
    lobby = game_manager.get_game(player)

    if not lobby.has_started():
        print('starting cards', lobby.get_name())
        cards = CardStack(lobby.get_players())
        lobby.start_game(cards)
        emit('goto_game', '/cards', room=lobby.get_name())

@socketio.on('game_started_cards')
def game_started_cards():
    player = request.remote_addr
    game = game_manager.get_game(player)
    join_room(game.get_name())

    player_data = []
    for p in game.get_players():
        if p != player:
            name = game_manager.player_name(p)
            player_data.append({'name': name, 'id': p})

    cards = game.get_game()
    data = json.dumps({'for': player, 'data': cards.get_stack_data(player), 
        'players': player_data})
    emit('reset_cards', data, room=game.get_name())
    print('Reset', player, 'cards')

def draw_random_card(player, game):
    cards = game.get_game()
    card = cards.draw_card(player)
    print('Gave player', player, 'card', card.get_id())
    return card

@socketio.on('draw_card')
def draw_card():
    player = request.remote_addr
    game = game_manager.get_game(player)
    if game != None:
        card = draw_random_card(player, game)
        data = json.dumps({'for': player, 'card': card.get_json_data()})
        emit('give_card', data, room=game.get_name())

@socketio.on('draw_card_down')
def draw_card_down():
    player = request.remote_addr
    game = game_manager.get_game(player)
    if game != None:
        card = draw_random_card(player, game)
        card.set_pos(0, 0, True)
        data = json.dumps({'for': player, 'card': card.get_json_data()})
        emit('give_card', data, room=game.get_name())

@socketio.on('update_position')
def update_position(card_id, x, y, back):
    player = request.remote_addr
    game = game_manager.get_game(player)
    if game != None:
        cards = game.get_game()
        cards.update_card_pos(player, card_id, x, y, back)
        print('Updated card', card_id, 'position to', x, y, back)

@socketio.on('give_card_to')
def give_card_to(card_id, to):
    player = request.remote_addr
    game = game_manager.get_game(player)
    if game != None:
        cards = game.get_game()
        card = cards.give(player, card_id, to)
        data = json.dumps({'for': to, 'card': card.get_json_data()})
        emit('give_card', data, room=game.get_name())
        print('Gave card', card_id, 'from', player, 'to', to)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='80')
