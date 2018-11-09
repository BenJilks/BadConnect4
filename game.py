
# Stores and handles data about one game
class Game:
    def __init__(self, name):
        self.__name = name
        self.__players = []
        self.__is_lobby = True
        self.__turn = 0
        self.__game = None
    
    def get_name(self):
        return self.__name
    
    def get_players(self):
        return self.__players

    def get_game(self):
        return self.__game

    # Adds a new player to the game
    def add_player(self, player):
        self.__players.append(player)
    
    def remove_player(self, player):
        self.__players.remove(player)

    # Returns if the game has started
    def has_started(self):
        return not self.__is_lobby
    
    # Starts the game
    def start_game(self, game):
        self.__is_lobby = False
        self.__game = game
    
    def end_game(self):
        self.__is_lobby = True

    # Returns if a player is in this game
    def is_game(self, player):
        return player in self.__players
    
    # Returns if it's this players turn
    def is_turn(self, player):
        return player == self.__players[self.__turn]
    
    def curr_player(self):
        return self.__players[self.__turn]
    
    # Sets the next turn
    def next_turn(self):
        self.__turn = (self.__turn + 1) % len(self.__players)

# Manages all current games
class GameManager:
    def __init__(self):
        self.__games = []
        self.__players = {}
    
    # Joins a player to a lobby by it's name
    def join_lobby(self, lobby_name, player):
        # If the player is already in a game
        curr_game = self.get_game(player)
        while curr_game != None:
            curr_game.remove_player(player)
            curr_game = self.get_game(player)

        # Find a lobby with that name
        for game in self.__games:
            if game.get_name() == lobby_name:
                game.add_player(player)
                return game
        
        game = Game(lobby_name)
        game.add_player(player)
        self.__games.append(game)
        return game        

    # Start the game of the lobby the player is in
    def start_game(self, player, game_data):
        game = self.get_game(player)
        if game == None:
            return False
        
        game.start_game(game_data)
        return True
    
    # Returns the current game of a player
    def get_game(self, player):
        for game in self.__games:
            if game.is_game(player):
                return game
        return None
    
    # Registers a new player under a name
    def register_player(self, player, name):
        self.__players[player] = name
    
    # Returns the name of a player
    def player_name(self, player):
        return self.__players[player]
