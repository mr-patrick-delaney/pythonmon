from pythonmon_data import pythonmon_data
from random import sample
from tabulate import tabulate
from rich import print

active_pythonmon = None
cpu_pythonmon = None
game_over = False

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
    
    def attack(self):
        if self.energy >= self._atk_energy:
            self.energy -= self._atk_energy
            return f'{active_pythonmon._name} used {active_pythonmon._atk_name}!'
        else:
            return '[yellow]Insufficient energy![/yellow]'
    
    def get_color(self):
        color_types = {
            'Fire': 'red',
            'Water': 'blue',
            'Grass': 'green'
        }
        return color_types[self._type]
    
    def get_damage(self, opponent):
        strengths = {
            'Fire': 'Grass',
            'Water': 'Fire',
            'Grass': 'Water'
        }

        if strengths[self._type] == opponent._type:
            return (self._atk_dmg * 2, '[purple bold]It\'s super effective![/purple bold]')
        return (self._atk_dmg,"")
    
    
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
                
            
print('Welcome to Pythonmon!')
print('Drawing decks...')
deck = Deck()
cpu_deck = Deck()
print('Dealing hands...')
hand = deck.deal_hand()
cpu_hand = cpu_deck.deal_hand()
print(hand)

while active_pythonmon is None:
    active_pythonmon = hand.play_card(input('Choose a Pythonmon to play: '))

cpu_pythonmon = sample(cpu_deck._cards,1)[0]

cpu_color = cpu_pythonmon.get_color()

color = active_pythonmon.get_color()

while game_over == False:

    print('[green]YOUR CARD:[/green]')
    print(active_pythonmon)
    print('[red]OPPONENT CARD[/red]')
    print(cpu_pythonmon)

    command = input('[C]harge energy, [A]ttack or [F]orfeit: ')
    if command.lower() in ['c', 'charge', 'charge energy']:
        print('-----------------')
        print(f'[yellow]{active_pythonmon._name} is charging energy...[/yellow]')
        print('-----------------')

        active_pythonmon.charge()
        
    elif command.lower() in ['a', 'atk', 'attack']:
        print('-----------------')
        print(f'[{color}]{active_pythonmon.attack()} [/{color}]')
        damage = active_pythonmon.get_damage(cpu_pythonmon)
        cpu_pythonmon._hp -= damage[0]
        if damage[1]:
            print(damage[1])
        print('-----------------')

    elif command.lower() in ['f', 'forfeit']:
        print('-----------------')
        print('You lose!')
        print('-----------------')
        game_over = True
        break




