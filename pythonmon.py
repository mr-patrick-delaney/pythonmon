# import files
from pythonmon_data import pythonmon_data
from random import sample
from tabulate import tabulate
from rich import print
from play_sounds import play_file


class Pythonmon():
    def __init__(self, name, type, hp, defense, atkname, atk_dmg, atk_energy, sound):
        self.name = name
        self._type = type
        self.hp = hp
        self._defense = defense
        self.atk_name = atkname
        self._atk_dmg = atk_dmg
        self.atk_energy = atk_energy
        self.sound = sound
        self.color = self._get_color()
        self.energy = 0

    def __str__(self):
        table = []
        headers = ['Name', 'Type', 'HP', 'Def', 'Attack', 'Dmg', 'Atk Energy', 'Energy']
        table.append([self.name, self._type, self.hp, self._defense, self.atk_name, self._atk_dmg, self.atk_energy,self.energy])
        return tabulate(table,headers=headers,tablefmt='grid')

    def charge(self):
        self.energy +=1
        return f'[yellow]{self.name} is charging energy...[/yellow]'
    
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

        if self.energy >= self.atk_energy:
            self.energy -= self.atk_energy
            attack['message'] = f'{self.name} used {self.atk_name}!'
            
            if strengths[self._type] == opponent._type:
                attack['dmg'] = (self._atk_dmg*2) - opponent._defense
                attack['effective'] = '[purple bold]It\'s super effective![/purple bold]'
            else:
                attack['dmg'] = self._atk_dmg - opponent._defense
        else:
            attack['message'] = '[yellow]Insufficient energy![/yellow]'
        
        return attack

    def _get_color(self):
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
        self.cards = cards

    def __str__(self):
        table = []
        headers = ['Name', 'Type', 'HP', 'Def', 'Attack', 'Dmg', 'Atk Energy']
        for card in self.cards:
            table.append([card.name, card._type, card.hp, card._defense, card.atk_name, card._atk_dmg, card.atk_energy])
        return tabulate(table,headers=headers,tablefmt='grid')

    def play_card(self,name):
        for index, card in enumerate(self.cards):
            if card.name.lower() == name.lower():
                return self.cards.pop(index)
            

def main():
    #define game variables
    active_pythonmon = None
    cpu_pythonmon = None
    game_over = False
    score = 0
    cpu_score = 0

    #game introduction and setup        
    print('Welcome to Pythonmon!')
    print('Drawing decks...')
    deck = Deck()
    cpu_deck = Deck()
    print('Dealing hands...')
    hand = deck.deal_hand()
    cpu_hand = cpu_deck.deal_hand()

    #show current hand to player
    print(hand)

    #player selects active pythonmon from hand
    while active_pythonmon is None:
        active_pythonmon = hand.play_card(input('Choose a Pythonmon to play: '))
        try:
            print('-----------------')
            print(f'You play [bold]{active_pythonmon.name}![/bold]')
            print('-----------------')
            play_file('sounds/'+active_pythonmon.sound,block=False)
        except:
            continue

    #cpu randomly chooses active pythonmon from hand
    cpu_pythonmon = sample(cpu_hand.cards,1)[0]
    cpu_hand.cards.remove(cpu_pythonmon)

    #start game loop
    while game_over == False:

        #check game over conditions - end game if true
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
        
        #display active and opponent active cards
        print('[green]YOUR ACTIVE CARD:[/green]')
        print(active_pythonmon)
        print('[red]OPPONENT ACTIVE CARD[/red]')
        print(cpu_pythonmon)

        #get turn command from player
        command = input('[C]harge Energy, [A]ttack, [V]iew Hand, [D]raw Card or [F]orfeit: ')

        #charge active pythonmon energy
        if command.lower() in ['c', 'charge', 'charge energy']:
            print('-----------------')
            print(active_pythonmon.charge())
            play_file('sounds/fx073.mp3')
            print('-----------------')

        #call attack method and return attack data
        elif command.lower() in ['a', 'atk', 'attack']:
            print('-----------------')
            attack = active_pythonmon.attack(cpu_pythonmon)
            print(f'[{active_pythonmon.color}]{attack['message']}[/{active_pythonmon.color}]')

            #if attack was successful, attack opponent pythonmon
            if attack['dmg']:
                cpu_pythonmon.hp -= attack['dmg']

                #display message if attack is super effective
                if attack['effective']:
                    print(attack['effective'])
                play_file('sounds/'+active_pythonmon.sound)
            print('-----------------')

        #show current hand
        elif command.lower() in ('v', 'view', 'view hand'):
            print('[green]CURRENT HAND[/green]')
            print(hand)

        #draw card from deck and add to hand if hand is less than 5 cards currently
        elif command.lower() in ['d', 'draw', 'draw card']:
            if len(hand.cards) < 5:
                deck.deal_card(hand)
                print('-----------------')
                print(f'Drew {hand.cards[-1].name} - {hand.cards[-1]._type} type Pythonmon')
                print('-----------------')
            else:
                print('-----------------')
                print('[red]Cannot have more than 5 cards in hand![/red]')
                print('-----------------')
        
        #forfeit game
        elif command.lower() in ['f', 'forfeit']:
            print('-----------------')
            print('You lose!')
            print('-----------------')
            game_over = True
            break
        
        #check if opponent pythonmon has fainted, if true, add 1 to player score
        if cpu_pythonmon.hp < 1:
            print('-----------------')
            print(f'[bold]{cpu_pythonmon.name} fainted...[/bold]')
            play_file('sounds/'+cpu_pythonmon.sound)
            print('-----------------')
            score +=1

            #opponent randomly plays new pythonmon if score is less than 3
            if score < 3:
                cpu_pythonmon = sample(cpu_hand.cards,1)[0]
                cpu_hand.cards.remove(cpu_pythonmon)
                print(f'Opponent plays [bold]{cpu_pythonmon.name}![/bold]')
                play_file('sounds/'+cpu_pythonmon.sound)
                print('-----------------')
        
        #CPU turn
        #opponent pythonmon charges energy if not enough energy to attack
        if cpu_pythonmon.energy < cpu_pythonmon.atk_energy:
            print('-----------------')
            print(f'[red bold]Opponent Pythonmon:[/red bold] {cpu_pythonmon.charge()}')
            print('-----------------')
            play_file('sounds/fx073.mp3')

        #call attack method and return attack data
        elif cpu_pythonmon.energy == cpu_pythonmon.atk_energy:
            print('-----------------')
            attack = cpu_pythonmon.attack(active_pythonmon)
            print(f'[red bold]Opponent Pythonmon: [/red bold][{cpu_pythonmon.color}]{attack['message']}[/{cpu_pythonmon.color}]')

            #if attack was successful, attack active player pythonmon
            if attack['dmg']:
                active_pythonmon.hp -= attack['dmg']

                #display message if attack is super effective
                if attack['effective']:
                    print(attack['effective'])
                play_file('sounds/'+cpu_pythonmon.sound)
            print('-----------------')

        #check if player active pythonmon has fainted, if true, add 1 to cpu score
        if active_pythonmon.hp < 1:
            print('-----------------')
            print(f'[bold]{active_pythonmon.name} fainted...[/bold]')
            play_file('sounds/'+active_pythonmon.sound)
            print('-----------------')
            cpu_score +=1

            #if cpu score is less than 3, player chooses a new pythonmon to play from hand
            active_pythonmon = None
            if cpu_score < 3:
                print(hand)
                while active_pythonmon is None:
                    active_pythonmon = hand.play_card(input('Choose a Pythonmon to play: '))
                    try:
                        print('-----------------')
                        print(f'You play [bold]{active_pythonmon.name}![/bold]')
                        print('-----------------')
                        play_file('sounds/'+active_pythonmon.sound,block=False)
                    except:
                        continue

if __name__ == "__main__":
    main()