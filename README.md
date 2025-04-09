 # PYTHONMON
   #### Description:
   My project is a Pokemon Trading Card Game (TCG) inspired game that aims to simulate the basic functionality of the popular TCG.

   In this game, the player competes against a computer opponent. The game starts by preparing a deck for both the player and the computer, and deals a five card hand to both the player and the computer. The player then chooses an 'active' Pythonmon card from their hand to play. The computer also randomly chooses a Pythonmon card to play. 
    
   Each turn starts with the player's action - the player can either 'Charge Energy', 'Attack' (if enough energy), 'Switch Pythonmon', 'Draw another card from the deck', or 'Forfeit'. After the player's turn, the game will check whether the computer's Pythonmon has fainted, before then commencing the computer's turn - who will either 'Charge Energy' or 'Attack' (if enough energy). 
    
   After the computer's turn, the game will check whether the player's Pythonmon has fainted - and if so, allow the Player to choose a new Pythonmon. The game will continue to loop in this fashion until either the Player wins (3 of the computer's Pythomon have fainted), or the computer wins (3 of the Player's Pytonmon have fainted or the player has forfeit the game).

   There are two main files:
   1. project.py - contains game functionality and classes - see detailed documentation within file for specific information
   2. pythonmon_data.py - contains data for 45 unique Pythonmon

   In addition, there is a directory of sounds which are used for sound effects in the game. Credit to __[jalastram](https://freesound.org/people/jalastram/)__ for the sounds. 

   This project uses the following external libraries:
   - tabluate - used to display Pythonmon data in a visually appealing maner within the Terminal
   - rich - used to display colored text in the game to make the game more visually appealling
   - play_sound - used to play a unique sound effect whenever a Pythonmon card is played, attacks or faints