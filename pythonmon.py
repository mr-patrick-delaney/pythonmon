from pythonmon_data import pythonmon_data
from random import sample

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
        return f'{self._name} - {self._type} Type Pythonmon'

    def charge(self):
        self.energy +=1
    
    
class Deck():

    def __init__(self):
        data = sample(pythonmon_data,20)
        self.cards = [Pythonmon(*datum) for datum in data]
    
    def __str__(self):
        return f'Deck of {len(deck.cards)} Pythonmon Cards'

deck = Deck()
print(deck)
for card in deck.cards:
    print(card)





