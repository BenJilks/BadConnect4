import random

class Card:
    def __init__(self, set_n, number, id):
        self.__set = set_n
        self.__number = number
        self.__id = id
        self.__x = 0
        self.__y = 0
    
    def get_set(self):
        return self.__set
    
    def get_number(self):
        return self.__number
    
    def get_id(self):
        return self.__id
    
    def set_pos(self, x, y):
        self.__x = x
        self.__y = y
    
    def get_pos(self):
        return self.__x, self.__y
    
    def get_json_data(self):
        return {'set': self.__set, 'number': self.__number, 
                'id': self.__id, 'x': self.__x, 'y': self.__y}

class CardStack:
    def __init__(self, players):
        self.__players = players
        self.__player_cards = {}
        self.__stack = []

        # Start players with empty stack
        for player in players:
            self.__player_cards[player] = []
        
        # Create a stack of cards
        ids = [-1]
        for i in range(4):
            for j in range(1, 13):
                id = -1
                while id in ids:
                    id = random.randint(0, 99999)
                card = Card(i, j, id)
                self.__stack.append(card)

    # Takes a random card from the stack    
    def draw_card(self, player):
        if len(self.__stack) <= 0:
            return None

        card = random.choice(self.__stack)
        self.__stack.remove(card)
        self.__player_cards[player].append(card)
        return card

    # Find a card in a players stack by its id
    def get_card_by_id(self, player, card_id):
        for card in self.__player_cards[player]:
            if card.get_id() == card_id:
                return card
        return None
    
    def give(self, player, card_id, to):
        card = self.get_card_by_id(player, card_id)
        self.__player_cards[player].remove(card)
        self.__player_cards[to].append(card)
        return card

    # Change the cards postion in a players stack by its id
    def update_card_pos(self, player, card_id, x, y):
        card = self.get_card_by_id(player, card_id)
        if card != None:
            card.set_pos(x, y)
    
    # Return all card data for a player
    def get_stack_data(self, player):
        data = []
        for card in self.__player_cards[player]:
            data.append(card.get_json_data())
        return data
