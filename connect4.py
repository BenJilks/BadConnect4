import random

class Board:
    def __init__(self, players, width, height):
        self.__width = width
        self.__height = height
        self.__grid = [[None 
            for x in range(width)] 
            for y in range(height)]
        
        # Assign player colours
        colour_list = ['red.png', 'yellow.png', 'blue.png', 'green.png']
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
                return True
        return False
    
    def get_data(self):
        return self.__grid
    
    def get_width(self):
        return self.__width
    
    def get_height(self):
        return self.__height
