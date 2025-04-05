from pythonmon_data import pythonmon_data
from random import sample
from tabulate import tabulate
from rich import print
from play_sounds import play_file

active_pythonmon = None
cpu_pythonmon = None
game_over = False
score = 0
cpu_score = 0

class Pythonmon():
    
    def __init__(self, name, type, hp, defense, atk_name, atk_dmg, atk_energy, sound):
        self._name = name
        self._type = type
        self._hp = hp
        self._defense = defense
        self._atk_name = atk_name
        self._atk_dmg = atk_dmg
        self._atk_energy = atk_energy
        self._sound = sound
        self.energy = 0

    def __str__(self):
        table = []
        headers = ['Name', 'Type', 'HP', 'Def', 'Attack', 'Dmg', 'Atk Energy', 'Energy']
        table.append([self._name, self._type, self._hp, self._defense, self._atk_name, self._atk_dmg, self._atk_energy,self.energy])
        return tabulate(table,headers=headers,tablefmt='grid')

    def charge(self):
        self.energy +=1
    
    def attack(self,opponent):
        attack = {
            'message': None,
            'dmg': None,
            'effective': None
        }

        strengths = {
            'Fire': 'Grass',
            'Water': 'Fire',
            'Grass': 'Water'
        }

        if self.energy >= self._atk_energy:
            self.energy -= self._atk_energy
            attack['message'] = f'{active_pythonmon._name} used {active_pythonmon._atk_name}!'
            
            if strengths[self._type] == opponent._type:
                attack['dmg'] = self._atk_dmg*2
                attack['effective'] = '[purple bold]It\'s super effective![/purple bold]'
            else:
                attack['dmg'] = self._atk_dmg
        else:
            attack['message'] = '[yellow]Insufficient energy![/yellow]'
        
        return attack

    def get_color(self):
        color_types = {
            'Fire': 'red',
            'Water': 'blue',
            'Grass': 'green'
        }
        return color_types[self._type]
    
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
        for index, card in enumerate(self._cards):
            if card._name.lower() == name.lower():
                return self._cards.pop(index)
            
                
            
print('Welcome to Pythonmon!')
print('Drawing decks...')
deck = Deck()
cpu_deck = Deck()
print('Dealing hands...')
hand = deck.deal_hand()
cpu_hand = cpu_deck.deal_hand()
print(cpu_hand)
print(hand)

while active_pythonmon is None:
    active_pythonmon = hand.play_card(input('Choose a Pythonmon to play: '))
    print('-----------------')
    print(f'You play [bold]{active_pythonmon._name}![/bold]')
    print('-----------------')
    play_file('sounds/'+active_pythonmon._sound,block=False)


cpu_pythonmon = sample(cpu_hand._cards,1)[0]
cpu_hand._cards.remove(cpu_pythonmon)

cpu_color = cpu_pythonmon.get_color()

color = active_pythonmon.get_color()

while game_over == False:
    print('[green]YOUR ACTIVE CARD:[/green]')
    print(active_pythonmon)
    print('[red]OPPONENT ACTIVE CARD[/red]')
    print(cpu_pythonmon)

    command = input('[C]harge Energy, [A]ttack, [V]iew Hand, [D]raw Card or [F]orfeit: ')
    if command.lower() in ['c', 'charge', 'charge energy']:
        print('-----------------')
        print(f'[yellow]{active_pythonmon._name} is charging energy...[/yellow]')
        play_file('sounds/fx073.mp3')
        print('-----------------')

        active_pythonmon.charge()
        
    elif command.lower() in ['a', 'atk', 'attack']:
        print('-----------------')
        attack = active_pythonmon.attack(cpu_pythonmon)
        print(f'[{color}]{attack['message']}[/{color}]')

        if attack['dmg']:
            cpu_pythonmon._hp -= attack['dmg']

            if attack['effective']:
                print(attack['effective'])
            play_file('sounds/'+active_pythonmon._sound)
        print('-----------------')

    elif command.lower() in ('v', 'view', 'view hand'):
        print('[green]CURRENT HAND[/green]')
        print(hand)

    elif command.lower() in ['d', 'draw', 'draw card']:
        if len(hand._cards) < 5:
            deck.deal_card(hand)
            print('-----------------')
            print(f'Drew {hand._cards[-1]._name} - {hand._cards[-1]._type} type Pythonmon')
            print('-----------------')
        else:
            print('-----------------')
            print('[red]Cannot have more than 5 cards in hand![/red]')
            print('-----------------')
    
    elif command.lower() in ['f', 'forfeit']:
        print('-----------------')
        print('You lose!')
        print('-----------------')
        game_over = True
        break

    if cpu_pythonmon._hp < 1:
        print('-----------------')
        print(f'[bold]{cpu_pythonmon._name} fainted...[/bold]')
        play_file('sounds/'+cpu_pythonmon._sound)
        print('-----------------')
        score +=1
        if score < 3:
            cpu_pythonmon = sample(cpu_hand._cards,1)[0]
            cpu_hand._cards.remove(cpu_pythonmon)
            print(f'Opponent plays [bold]{cpu_pythonmon._name}![/bold]')
            play_file('sounds/'+cpu_pythonmon._sound)
            print('-----------------')
    
    if score == 3:
        print('-----------------')
        print('You WIN!')
        print('-----------------')
        break

    elif cpu_score == 3:
        print('-----------------')
        print('You lose')
        print('-----------------')
        break
