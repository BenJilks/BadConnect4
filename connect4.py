import random

class Connect4Board:
    def __init__(self, players, width, height, connect):
        self.__width = width
        self.__height = height
        self.__connect = connect
        self.__grid = [[None 
            for x in range(width)] 
            for y in range(height)]
        self.__player_won = None
        
        # Assign player colours
        colour_list = ['red.png', 'yellow.png', 'blue.png', 'green.png']
        self.__players = players
        self.__colours = {}
        for player in players:
            colour = random.choice(colour_list)
            colour_list.remove(colour)
            self.__colours[player] = colour

    def player_colour(self, player):
        return self.__colours[player]

    def place(self, x, player):
        for y in range(self.__height - 1, -1, -1):
            if self.__grid[y][x] == None:
                self.__grid[y][x] = self.__colours[player]
                self.__player_won = self.check_won()
                return True
        return False
    
    def check_rows(self, colour):
        for row in self.__grid:
            for i in range(self.__width - self.__connect + 1):
                is_full = True
                for j in range(self.__connect):
                    if row[i + j] != colour:
                        is_full = False
                        break
                
                if is_full:
                    return True
        return False
    
    def check_coloumns(self, colour):
        for x in range(self.__width):
            for i in range(self.__height - self.__connect + 1):
                is_full = True
                for j in range(self.__connect):
                    if self.__grid[i + j][x] != colour:
                        is_full = False
                        break
                
                if is_full:
                    return True
        return False

    def check_cross(self, colour):
        for x in range(self.__width - self.__connect + 1):
            for y in range(self.__height - self.__connect + 1):
                is_full = True
                for i in range(self.__connect):
                    if self.__grid[y+i][x+i] != colour:
                        is_full = False
                        break
                
                if is_full:
                    return True
        
        for x in range(3, self.__width):
            for y in range(self.__height - self.__connect + 1):
                is_full = True
                for i in range(self.__connect):
                    if self.__grid[y+i][x-i] != colour:
                        is_full = False
                        break
                
                if is_full:
                    return True
        return False

    def check_won(self):
        for player in self.__players:
            colour = self.player_colour(player)
            is_row = self.check_rows(colour)
            is_column = self.check_coloumns(colour)
            is_cross = self.check_cross(colour)
            if is_row or is_column or is_cross:
                return player
        return None

    def has_won(self):
        return self.__player_won

    def get_data(self):
        return self.__grid
    
    def get_width(self):
        return self.__width
    
    def get_height(self):
        return self.__height
