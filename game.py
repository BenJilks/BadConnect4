
# Stores and handles data about one game
class Game:
    def __init__(self, players):
        self.__players = players
        self.__turn = 0
    
    # Returns if a player is in this game
    def is_game(self, player):
        return player in self.__players
    
    # Returns if it's this players turn
    def is_turn(self, player):
        return player == self.__players[self.__turn]
    
    # Sets the next turn
    def next_turn(self):
        self.__turn = (self.__turn + 1) % len(self.__players)

# All players about to join a game go into a lobby first
class Lobby:
    def __init__(self, name):
        self.__name = name
        self.__players = []
    
    # Adds a player to a lobby
    def add_player(self, player):
        self.__players.append(player)
    
    # Returns if a player is in this lobby
    def is_lobby(self, player):
        return player in self.__players

    # Returns the list of players in the lobby
    def get_players(self):
        return self.__players
    
    # Returns the lobby name
    def get_name(self):
        return self.__name

# Manages all current games
class GameManager:
    def __init__(self):
        self.__games = []
        self.__lobbies = []
    
    # Joins a player to a lobby by it's name, 
    # if the lobby does not exist then create it
    def join_lobby(self, lobby_name, player):
        # Find a lobby with that name
        for lobby in self.__lobbies:
            if lobby.get_name() == lobby_name:
                lobby.add_player(player)
                return lobby
        
        # If no lobby could be found, make one
        lobby = Lobby(lobby_name)
        lobby.add_player(player)
        self.__lobbies.append(lobby)
        return lobby

    # Start the game of the lobby the player is in
    def start_game(self, player):
        curr_lobby = None
        for lobby in self.__lobbies:
            if lobby.is_lobby(player):
                curr_lobby = lobby
                break
        
        if curr_lobby == None:
            return False
        
        # Create a new game and remove the lobby
        game = Game(curr_lobby.get_players())
        self.__games.append(game)
        self.__lobbies.remove(curr_lobby)
        return True
    
    # Returns the current game of a player
    def get_game(self, player):
        for game in self.__games:
            if game.is_game(player):
                return game
        return None
