 # PYTHONMON
    #### Video Demo:  <URL HERE>
    #### Description:
    My project is a Pokemon Trading Card Game (TCG) inspired game that aims to simulate the basic functionality of the popular TCG.

    In this game, the player competes against a computer opponent. The game starts by preparing a deck for both the player and the computer, and deals a five card hand to both the player and the computer. The player then chooses an 'active' Pythonmon card from their hand to play. The computer also randomly chooses a Pythonmon card to play. 
    
    Each turn starts with the player's action - the player can either 'Charge Energy', 'Attack' (if enough energy), 'Switch Pythonmon', 'Draw another card from the deck', or 'Forfeit'. After the player's turn, the game will check whether the computer's Pythonmon has fainted, before then commencing the computer's turn - who will either 'Charge Energy' or 'Attack' (if enough energy). 
    
    After the computer's turn, the game will check whether the player's Pythonmon has fainted - and if so, allow the Player to choose a new Pythonmon. The game will continue to loop in this fashion until either the Player wins (3 of the computer's Pythomon have fainted), or the computer wins (3 of the Player's Pytonmon have fainted or the player has forfeit the game).

    There are two main files:
    - project.py - contains game functionality and classes - see detailed documentation within file for specific information
    - pythonmon_data.py - contains data for 45 unique Pythonmon

    In addition, there is a directory of sounds which are used for sound effects in the game. Credit to jalastram for sounds (https://freesound.org/people/jalastram/).

    This project uses the following external libraries:
    - tabluate - used to display Pythonmon data in a visually appealing maner within the Terminal
    - rich - used to display colored text in the game to make the game more visually appealling
    - play_sound - used to play a unique sound effect whenever a Pythonmon card is played, attacks or faints

    My design started with planning out the three classes: Pythonmon, Deck and Hand - and getting the methods for each of these classes working. Once this was achieved, I then slowly began to develop the 'game loop' with the idea of the 'active Pythonmon' and the 'CPU pythonmon' facing off against one another. I iteratively added additional functionality to the game, bit by bit, and tested the game after each new functionality. Once the 'game loop' was finished, I then sought to refactor the code into distinct functions and helper functions to reduce the size of the 'game loop' and remove repeated code.

    Further areas for improvement include:
    - adding a Game_State class to track the state of the game rather than have it all done within main()
    - making the CPU AI logic more complex (ie. CPU switching out Pythonmon to take advantage of elemental weaknesses)