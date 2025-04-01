from random import sample

pythonmon_data = [
    ['Scanpan', 'Fire', 30, 2, 'Fire Blast', 5, 2],
    ['Basmati', 'Water', 35, 2, 'Water Jet', 4, 2]
]


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
        data = sample(pythonmon_data,2)
        self.cards = [Pythonmon(*datum) for datum in data]
    
    def __str__(self):
        return f'Deck of {len(deck.cards)} Pythonmon Cards'

deck = Deck()
print(deck)
print(deck.cards[0])
print(deck.cards[1])





