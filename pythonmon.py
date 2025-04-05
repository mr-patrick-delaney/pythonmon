from pythonmon_data import pythonmon_data
from random import sample
from tabulate import tabulate

active_pythonmon = None

class Pythonmon():
    
    def __init__(self, name, type, hp, defense, atk_name, atk_dmg, atk_energy):
        self._name = name
        self._type = type
        self._hp = hp
        self._defense = defense
        self._atk_name = atk_name
        self._atk_dmg = atk_dmg
        self._atk_energy = atk_energy
        self.energy = 0

    def __str__(self):
        table = []
        headers = ['Name', 'Type', 'HP', 'Def', 'Attack', 'Dmg', 'Atk Energy', 'Energy']
        table.append([self._name, self._type, self._hp, self._defense, self._atk_name, self._atk_dmg, self._atk_energy,self.energy])
        return tabulate(table,headers=headers,tablefmt='grid')

    def charge(self):
        self.energy +=1
    
    
class Deck():

    def __init__(self):
        data = sample(pythonmon_data,20)
        self._cards = [Pythonmon(*datum) for datum in data]
    
    def __str__(self):
        return f'Deck of {len(self._cards)} Pythonmon Cards'
    
    def deal_hand(self):
        hand_cards = self._cards[-5:]
        self._cards = self._cards[:-5]
        return Hand(hand_cards)
    
    def deal_card(self, hand):
        hand_card = self._cards[-1]
        self._cards = self._cards[:-1]
        hand._cards.append(hand_card)
        

class Hand():

    def __init__(self, cards):
        self._cards = cards

    def __str__(self):
        table = []
        headers = ['Name', 'Type', 'HP', 'Def', 'Attack', 'Dmg', 'Atk Energy']
        for card in self._cards:
            table.append([card._name, card._type, card._hp, card._defense, card._atk_name, card._atk_dmg, card._atk_energy])
        return tabulate(table,headers=headers,tablefmt='grid')

    
    def play_card(self,name):
        for card in self._cards:
            if card._name == name:
                return card
                
            


deck = Deck()
hand = deck.deal_hand()

print('Welcome to Pythonmon!')
print('Drawing deck...')
deck = Deck()
print('Dealing hand...')
hand = deck.deal_hand()
print(hand)
while active_pythonmon is None:
    active_pythonmon = hand.play_card(input('Choose a Pythonmon to play: '))
print(active_pythonmon)






