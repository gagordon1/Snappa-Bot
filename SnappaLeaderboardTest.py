
from SnappaLeaderboard import SnappaLeaderboard, generate_leaderboard_string
from GoogleSheetsDatabase import GoogleSheetsDatabase
from GoogleSheetsDatabaseTest import initialize_game_log, initialize_player_sheet
from tabulate import tabulate
from elosports.elo import Elo
INITIAL_ELO = 1500
SPREADSHEET_NAME = "Snappa Database"
PLAYER_SHEET_INDEX = 2
GAME_SHEET_INDEX = 3


def addPlayerTest1():
    """Add a player and verify that the leaderboard was updated

    Returns
    -------
    Boolean
        True if behaves correctly, False otherwise

    """
    db = GoogleSheetsDatabase(PLAYER_SHEET_INDEX, GAME_SHEET_INDEX)
    leaderboard = SnappaLeaderboard(db)
    name = "Garrett"
    name2 = "Andrei"
    data1 = [["Garrett", INITIAL_ELO, 0,0]]
    data2 = [["Garrett", INITIAL_ELO, 0,0], ["Andrei", INITIAL_ELO, 0, 0]]
    n = 2
    response = leaderboard.add_player(name)
    if response != "Player Garrett successfully added to the database!":
        return False

    lb = leaderboard.get_leaderboard(n)

    #TEST1

    if lb != generate_leaderboard_string(data1, n):
        return False

    leaderboard.add_player(name2)
    lb2 = leaderboard.get_leaderboard(n)
    if lb2 != generate_leaderboard_string(data2, n):
        return False

    return True



def logScoreTest1():
    """Add two scores and verify that the leaderboard was properly updated

    Returns
    -------
    Boolean
        True if behaves correctly, False otherwise

    """
    db = GoogleSheetsDatabase(PLAYER_SHEET_INDEX, GAME_SHEET_INDEX)
    names = ["Garrett", "Andrei", "Noah", "Sebastian"]
    data2 = [[names[0], INITIAL_ELO, 0,0], [names[1], INITIAL_ELO, 0, 0],
    [names[2], INITIAL_ELO, 0, 0], [names[3], INITIAL_ELO, 0, 0]]
    leaderboard = SnappaLeaderboard(db)
    for name in names:
        leaderboard.add_player(name)

    response = leaderboard.log_score(*names, 7, 5)
    expected = "TBU"

    if response != expected:
        return False

    response = leaderboard.log_score(*names, 3, 7)
    expected = "TBU"

    if response != expected:
        return False

    return True


def getPlayerHistoryTest1():
    """Adds players, log some games then verifies a correct player
    history

    Returns
    -------
    Boolean
        True if behaves correctly, False otherwise


    """
    return False

if __name__ == '__main__':
    initialize_game_log()
    initialize_player_sheet()
    for name, test in [["Add Player Test 1", addPlayerTest1],
            ["Log Score Test 1", logScoreTest1],
            ["Get Player History Test 1", getPlayerHistoryTest1]]:
        if test():
            print(str(name) + " passed!")
        else:
            print(str(name) + " failed!")
