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
        print('-----------------')
        print(f'[yellow]{self.name} is charging energy...[/yellow]')
        play_file('sounds/fx073.mp3')
        print('-----------------')
    
    def attack(self,opponent):
        strengths = {
            'Fire': 'Grass',
            'Water': 'Fire',
            'Grass': 'Water'
        }

        if self.energy >= self.atk_energy:
            self.energy -= self.atk_energy
            print('-----------------')
            print(f'[{self.color}]{self.name} used {self.atk_name}![/{self.color}]')
            
            if strengths[self._type] == opponent._type:
                opponent.hp -= (self._atk_dmg*2) - opponent._defense
                print('[purple bold]It\'s super effective![/purple bold]')
            else:
                opponent.hp -= self._atk_dmg - opponent._defense
            play_file('sounds/'+self.sound)
        else:
            print('[yellow]Insufficient energy![/yellow]')

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
        if len(hand.cards) < 4:
            hand_card = self._cards[-1]
            self._cards = self._cards[:-1]
            hand.cards.append(hand_card)
            print('-----------------')
            print(f'Drew {hand.cards[-1].name}!')
            print(hand.cards[-1])
            print('-----------------')
        else:
            print('-----------------')
            print('[red]Cannot have more than 5 cards in hand![/red]')
            print('-----------------')
        

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


def initialise_game():
    print('Welcome to Pythonmon!')
    print('Drawing decks...')
    deck = Deck()
    cpu_deck = Deck()
    print('Dealing hands...')
    hand = deck.deal_hand()
    cpu_hand = cpu_deck.deal_hand()
    return deck, hand, cpu_hand

def select_pythonmon(hand):
        while True:
            selected = hand.play_card(input('Choose a Pythonmon to play: '))
            try:
                print('-----------------')
                print(f'You play [bold]{selected.name}![/bold]')
                print('-----------------')
                play_file('sounds/'+selected.sound,block=False)
            except:
                continue
            else:
                return selected

def check_game_over(score,cpu_score):
    if score == 3:
        print('-----------------')
        print('You WIN!')
        print('-----------------')
        return True
    elif cpu_score == 3:
        print('-----------------')
        print('You lose')
        print('-----------------')
        return True
    return False

def switch_pythonmon(active_pythonmon, hand):
    print(f'[bold]{active_pythonmon.name} return![/bold]')
    hand.cards.append(active_pythonmon)
    print('[green]CURRENT HAND[/green]')
    print(hand)
    return select_pythonmon(hand)


def player_turn(player, opponent, hand, deck):
    #display active and opponent active cards
    print('[green]YOUR ACTIVE CARD:[/green]')
    print(player)
    print('[red]OPPONENT ACTIVE CARD[/red]')
    print(opponent)

    #get turn command from player
    VALID_COMMANDS = ('c', 'charge', 'charge energy','a', 'atk', 'attack','s', 'switch', 'switch pythonmon','d', 'draw', 'draw card','f', 'forfeit')
    command = ""
    while command not in VALID_COMMANDS:
        command = input('[C]harge Energy, [A]ttack, [S]witch Pythonmon, [D]raw Card or [F]orfeit: ')

    #charge active pythonmon energy
    if command.lower() in ['c', 'charge', 'charge energy']:
        player.charge()

    #call attack method on opponent
    elif command.lower() in ['a', 'atk', 'attack']:
        player.attack(opponent)
    
    #switch active pythonmon
    elif command.lower() in ('s', 'switch', 'switch pythonmon'):
        player = switch_pythonmon(player,hand)

    #draw card from deck and add to hand if hand is less than 5 cards currently
    elif command.lower() in ['d', 'draw', 'draw card']:
        deck.deal_card(hand)
    
    #forfeit game - return True to game_over
    elif command.lower() in ['f', 'forfeit']:
        print('-----------------')
        print('You lose!')
        print('-----------------')
        return True, player
    
    #else return False to game_over to continue the game
    return False, player

def check_cpu_fainted(pythonmon,cpu_hand,score):
    if pythonmon.hp < 1:
        print('-----------------')
        print(f'[bold]{pythonmon.name} fainted...[/bold]')
        play_file('sounds/'+pythonmon.sound)
        print('-----------------')
        score +=1

        #opponent randomly plays new pythonmon if score is less than 3
        if score < 3:
            pythonmon = sample(cpu_hand.cards,1)[0]
            cpu_hand.cards.remove(pythonmon)
            print(f'Opponent plays [bold]{pythonmon.name}![/bold]')
            play_file('sounds/'+pythonmon.sound)
            print('-----------------')
    return pythonmon,score

def check_player_fainted(pythonmon,hand,cpu_score):
    if pythonmon.hp < 1:
        print('-----------------')
        print(f'[bold]{pythonmon.name} fainted...[/bold]')
        play_file('sounds/'+pythonmon.sound)
        print('-----------------')
        cpu_score +=1

        #if cpu score is less than 3, player chooses a new pythonmon to play from hand
        if cpu_score < 3:
            print(hand)
            pythonmon = select_pythonmon(hand)
    return pythonmon,cpu_score

def cpu_turn(opponent,player):
    #opponent pythonmon charges energy if not enough energy to attack
    print('-----------------')
    print('[red bold]Opponent Pythonmon: [/red bold]')
    if opponent.energy < opponent.atk_energy:
        opponent.charge()

    #call attack method on player
    elif opponent.energy == opponent.atk_energy:
        opponent.attack(player)


def main():
    #initialise game variables
    active_pythonmon = None
    cpu_pythonmon = None
    game_over = False
    score = 0
    cpu_score = 0

    #intialise player and cpu decks and hands
    deck, hand, cpu_hand = initialise_game()

    #show current hand to player
    print(hand)

    #player selects active pythonmon from hand
    while active_pythonmon is None:
        active_pythonmon = select_pythonmon(hand)

    #cpu randomly chooses active pythonmon from hand
    cpu_pythonmon = sample(cpu_hand.cards,1)[0]
    cpu_hand.cards.remove(cpu_pythonmon)

    #start game loop
    while not game_over:

        #check game over conditions before player turn, end game if true
        if check_game_over(score, cpu_score):
            break
        
        #execute player turn
        game_over,active_pythonmon = player_turn(active_pythonmon, cpu_pythonmon, hand, deck)

        #quit game if game over
        if game_over:
            break

        #check if opponent pythonmon has fainted, if true, add 1 to player score
        cpu_pythonmon, score = check_cpu_fainted(cpu_pythonmon,cpu_hand,score)
        
        #check game over conditions before CPU turn, end game if true
        if check_game_over(score, cpu_score):
            break

        #execute cpu turn
        cpu_turn(cpu_pythonmon,active_pythonmon)

        #check if player active pythonmon has fainted, if true, add 1 to cpu score
        active_pythonmon, cpu_score = check_player_fainted(active_pythonmon, hand,cpu_score)

if __name__ == "__main__":
    main()