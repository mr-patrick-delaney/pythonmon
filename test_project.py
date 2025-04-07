from pythonmon import Deck, Hand, Pythonmon
from pythonmon import initialise_game, select_pythonmon, check_game_over, switch_pythonmon, check_cpu_fainted, check_player_fainted
from unittest.mock import patch


def test_initialise_game():
    deck, hand, cpu_hand = initialise_game()
    assert isinstance(deck, Deck)
    assert isinstance(hand, Hand)
    assert isinstance(cpu_hand, Hand)

def test_select_pythonmon():
    mock_card = Pythonmon("Testmon", "Fire", 10, 1, "Flame", 3, 1, "fx026.mp3")
    hand = Hand([mock_card])

    with patch("builtins.input", return_value="Testmon"):
        result = select_pythonmon(hand)

    assert isinstance(result, Pythonmon)
    assert result.name == "Testmon"

def test_check_game_over_false():
    assert check_game_over(2,0) == False

def test_check_game_over_player_win():
    assert check_game_over(3,2) == True

def test_check_game_over_cpu_win():
    assert check_game_over(1,3) == True
 
def test_switch_pythonmon():
    mock_card = Pythonmon("Testmon", "Fire", 10, 1, "Flame", 3, 1, "fx026.mp3")
    active_pythonmon = Pythonmon("Activemon", "Water", 10, 1, "Wave", 3, 1, "fx026.mp3")
    hand = Hand([mock_card])

    with patch("builtins.input", return_value="Testmon"):
        result = switch_pythonmon(active_pythonmon,hand)

    assert isinstance(result, Pythonmon)
    assert result.name == "Testmon"

def test_check_cpu_fainted_false():
    mock_card = Pythonmon("Testmon", "Fire", 10, 1, "Flame", 3, 1, "fx026.mp3")
    pythonmon = Pythonmon("Activemon", "Water", 10, 1, "Wave", 3, 1, "fx026.mp3")
    cpu_hand = Hand([mock_card])
    score = 0
    
    result = check_cpu_fainted(pythonmon,cpu_hand,score)

    assert isinstance(result[0], Pythonmon)
    assert result[0].name == "Activemon"
    assert result[1] == 0

def test_check_cpu_fainted_true():
    mock_card = Pythonmon("Testmon", "Fire", 10, 1, "Flame", 3, 1, "fx026.mp3")
    pythonmon = Pythonmon("Activemon", "Water", 0, 1, "Wave", 3, 1, "fx026.mp3")
    cpu_hand = Hand([mock_card])
    score = 0
    
    result = check_cpu_fainted(pythonmon,cpu_hand,score)

    assert isinstance(result[0], Pythonmon)
    assert result[0].name == "Testmon"
    assert result[1] == 1

def test_check_player_fainted_false():
    mock_card = Pythonmon("Testmon", "Fire", 10, 1, "Flame", 3, 1, "fx026.mp3")
    pythonmon = Pythonmon("Activemon", "Water", 10, 1, "Wave", 3, 1, "fx026.mp3")
    hand = Hand([mock_card])
    cpu_score = 0
    
    result = check_player_fainted(pythonmon,hand,cpu_score)

    assert isinstance(result[0], Pythonmon)
    assert result[0].name == "Activemon"
    assert result[1] == 0

def test_check_player_fainted_true():
    mock_card = Pythonmon("Testmon", "Fire", 10, 1, "Flame", 3, 1, "fx026.mp3")
    pythonmon = Pythonmon("Activemon", "Water", 0, 1, "Wave", 3, 1, "fx026.mp3")
    hand = Hand([mock_card])
    cpu_score = 0
    
    with patch("builtins.input", return_value="Testmon"):
        result = check_player_fainted(pythonmon,hand,cpu_score)

    assert isinstance(result[0], Pythonmon)
    assert result[0].name == "Testmon"
    assert result[1] == 1