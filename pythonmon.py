# import files
from pythonmon_data import pythonmon_data
from random import sample
from tabulate import tabulate
from rich import print
from play_sounds import play_file


class Pythonmon():
    """
    Represents a Pythonmon card used in battle.

    Attributes:
        name (str): The Pythonmon's name.
        _type (str): The Pythonmon's elemental type ('Fire', 'Water', or 'Grass').
        hp (int): The Pythonmon's current health points.
        _defense (int): The defense value that reduces incoming damage.
        atk_name (str): The name of the Pythonmon's attack move.
        _atk_dmg (int): The base damage of the attack.
        atk_energy (int): The amount of energy required to perform the attack.
        sound (str): Filename of the Pythonmon's unique sound.
        color (str): Display color based on type ('red', 'blue', or 'green').
        energy (int): The current stored energy for attacks.

    Example:
        >>> pythonmon = Pythonmon('Scanpan', 'Fire', 23, 2, 'Fire Blast', 7, 3, 'fx026.mp3')
    """

    def __init__(self, name:str, type:str, hp:int, defense:int, atk_name:str, atk_dmg:int, atk_energy:int, sound:str):
        self.name = name
        self._type = type
        self.hp = hp
        self._defense = defense
        self.atk_name = atk_name
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
        """
        Charges the Pythonmon's energy by 1 point.

        Returns:
            None
        """

        self.energy +=1
        print('-----------------')
        print(f'[yellow]{self.name} is charging energy...[/yellow]')
        play_file('sounds/fx073.mp3')
        print('-----------------')
    
    def attack(self,opponent:"Pythonmon"):
        """
        Attacks the opponent Pythonmon if enough energy is available.

        Args:
            opponent (Pythonmon): The opponent Pythonmon to attack.

        Returns:
            None
        """

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

    def _get_color(self) -> str:
        """
        Determines the display color based on the Pythonmon's type.

        Returns:
            str: The color name ('red', 'blue', or 'green').
        """

        color_types = {
            'Fire': 'red',
            'Water': 'blue',
            'Grass': 'green'
        }
        return color_types[self._type]


class Deck():
    """
    Represents a deck containing 20 randomly drawn Pythonmon cards.

    Attributes:
        _cards (list[Pythonmon]): A list of Pythonmon cards currently in the deck.

    Example:
        >>> deck = Deck()
    """

    def __init__(self):
        data = sample(pythonmon_data,20)
        self._cards = [Pythonmon(*datum) for datum in data]
    
    def __str__(self):
        return f'Deck of {len(self._cards)} Pythonmon Cards'
    
    def deal_hand(self) -> "Hand":
        """
        Deals the last 5 cards from the deck as a starting hand.

        Returns:
            Hand: A Hand object containing 5 Pythonmon cards dealt from the deck.
        """

        hand_cards = self._cards[-5:]
        self._cards = self._cards[:-5]
        return Hand(hand_cards)
    
    def deal_card(self, hand:"Hand"):
        """
        Deals one card from the deck and adds it to the given hand, if hand has fewer than 5 cards.

        Args:
            hand (Hand): The hand that will receive the dealt Pythonmon card.
        """

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
    """
    Represents a player's hand of Pythonmon cards.

    Attributes:
        cards (list[Pythonmon]): A list of Pythonmon cards currently in the hand. Max of 5 cards.

    Example:
        >>> hand = Hand(cards)
    """

    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        table = []
        headers = ['Name', 'Type', 'HP', 'Def', 'Attack', 'Dmg', 'Atk Energy']
        for card in self.cards:
            table.append([card.name, card._type, card.hp, card._defense, card.atk_name, card._atk_dmg, card.atk_energy])
        return tabulate(table,headers=headers,tablefmt='grid')

    def play_card(self,name:str) -> Pythonmon:
        """
        Removes and returns the specified Pythonmon card from the hand by name.

        Args:
            name (str): The name of the Pythonmon card to play.

        Returns:
            Pythonmon: The selected Pythonmon card removed from the hand.
        """

        for index, card in enumerate(self.cards):
            if card.name.lower() == name.lower():
                return self.cards.pop(index)


def initialise_game() -> tuple[Deck, Hand, Hand]:
    """
    Introduces the game, and deals decks and hands for both the player and the CPU.

    Returns:
        tuple: A tuple containing:
            - deck (Deck): The player's deck.
            - hand (Hand): The player's starting hand.
            - cpu_hand (Hand): The CPU's starting hand.
    """

    print('Welcome to Pythonmon!')
    print('Drawing decks...')
    deck = Deck()
    cpu_deck = Deck()
    print('Dealing hands...')
    hand = deck.deal_hand()
    cpu_hand = cpu_deck.deal_hand()
    return deck, hand, cpu_hand

def select_pythonmon(hand:"Hand") -> Pythonmon:
    """
    Prompts the player to select a Pythonmon card from their current hand.

    Args:
        hand (Hand): The player's current hand.

    Returns:
        Pythonmon: The selected Pythonmon card.
    """

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

def check_game_over(score:int,cpu_score:int) -> bool:
    """
    Checks whether the game is over. The game ends when either player or CPU reaches 3 points.

    Args:
        score (int): The player's current score.
        cpu_score (int): The CPU's current score.

    Returns:
        bool: True if the game is over, False otherwise.
    """

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

def switch_pythonmon(active_pythonmon:Pythonmon, hand:Hand) -> Pythonmon:
    """
    Switches the current active Pythonmon with another from the player's hand.

    Args:
        active_pythonmon (Pythonmon): The player's currently active Pythonmon.
        hand (Hand): The player's current hand.

    Returns:
        Pythonmon: The newly selected Pythonmon from the hand.
    """

    print(f'[bold]{active_pythonmon.name} return![/bold]')
    hand.cards.append(active_pythonmon)
    print('[green]CURRENT HAND[/green]')
    print(hand)
    return select_pythonmon(hand)


def player_turn(player:Pythonmon, opponent:Pythonmon, hand:Hand, deck:Deck) -> tuple[bool,Pythonmon]:
    """
    Executes the player's turn based on input command.

    Args:
        player (Pythonmon): The player's active Pythonmon.
        opponent (Pythonmon): The opponent's active Pythonmon.
        hand (Hand): The player's hand.
        deck (Deck): The player's deck.

    Returns:
        tuple:
            bool: True if the player forfeits (game over), False otherwise.
            Pythonmon: The player's active Pythonmon at the end of their turn.
    """

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

def check_cpu_fainted(pythonmon:Pythonmon,cpu_hand:Hand,score:int) -> tuple[Pythonmon,int]:
    """
    Checks if the CPU's active Pythonmon has fainted (HP < 1). Increments the player's score if true.

    Args:
        pythonmon (Pythonmon): The CPU's current active Pythonmon.
        cpu_hand (Hand): The CPU's hand.
        score (int): The player's current score.

    Returns:
        tuple:
            Pythonmon: The CPU's active Pythonmon (either existing or replaced).
            int: The updated player score.
    """
        
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

def cpu_turn(opponent:Pythonmon,player:Pythonmon):
    """
    Executes the CPU's turn using basic AI logic. Charges energy or attacks based on current energy level.

    Args:
        opponent (Pythonmon): The CPU's active Pythonmon.
        player (Pythonmon): The player's active Pythonmon.
    """

    #opponent pythonmon charges energy if not enough energy to attack
    print('-----------------')
    print('[red bold]Opponent Pythonmon: [/red bold]')
    if opponent.energy < opponent.atk_energy:
        opponent.charge()

    #call attack method on player
    elif opponent.energy == opponent.atk_energy:
        opponent.attack(player)

def check_player_fainted(pythonmon:Pythonmon,hand:Hand,cpu_score:int) -> tuple[Pythonmon,int]:
    """
    Checks if the player's active Pythonmon has fainted (HP < 1). Increments CPU's score and prompts the player to choose a new Pythonmon if applicable.

    Args:
        pythonmon (Pythonmon): The player's current active Pythonmon.
        hand (Hand): The player's current hand.
        cpu_score (int): The CPU's current score.

    Returns:
        tuple:
            Pythonmon: The player's new active Pythonmon if fainted.
            int: The updated CPU score.
    """
        
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


def main():
    """
    Runs the main game loop for Pythonmon.

    Handles game initialisation, player/CPU turns, scoring, and win condition.
    """

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