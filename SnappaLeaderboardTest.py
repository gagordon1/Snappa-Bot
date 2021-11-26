
from SnappaLeaderboard import SnappaLeaderboard
from SnappaLeaderboardTextGenerator import generate_leaderboard_string, generate_score_log_string
from GoogleSheetsDatabase import GoogleSheetsDatabase
from GoogleSheetsDatabaseTest import initialize_game_log, initialize_player_sheet
from tabulate import tabulate
from elosports.elo import Elo
INITIAL_ELO = 1500
SPREADSHEET_NAME = "Snappa Database"
PLAYER_SHEET_INDEX = 2
GAME_SHEET_INDEX = 3


def addPlayerTest1(db):
    """Add a player and verify that the leaderboard was updated

    Returns
    -------
    Boolean
        True if behaves correctly, False otherwise

    """
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

    leaderboard.add_player("Noah")
    leaderboard.add_player("Sebastian")

    return True



def logScoreTest1(db):
    """Add two scores and verify that the leaderboard was properly updated

    Returns
    -------
    Boolean
        True if behaves correctly, False otherwise

    """
    names1 = ["Garrett", "Andrei", "Noah", "Sebastian"]
    names2 = ["Garrett", "Noah", "Andrei", "Sebastian"]
    leaderboard = SnappaLeaderboard(db)

    print(names1, 7, 5, ":")
    response = leaderboard.log_score(*names1, 7, 5)
    print(response)

    for i in range(3):
        print(names2, 3, 7, ":")
        response = leaderboard.log_score(*names2, 3, 7)
        print(response)

    return True


def getPlayerHistoryTest1(db):
    """Adds players, log some games then verifies a correct player
    history

    Returns
    -------
    Boolean
        True if behaves correctly, False otherwise


    """

    slb = SnappaLeaderboard(db)
    print(slb.generate_message())
    return True

if __name__ == '__main__':

    ### GOOGLE SHEETS TEST ####
    db = GoogleSheetsDatabase(test = True)

    for name, test in [
            ["Add Player Test 1", addPlayerTest1],
            ["Log Score Test 1", logScoreTest1],
            ["Get Player History Test 1", getPlayerHistoryTest1]]:
        if test(db):
            print(str(name) + " passed!")
        else:
            print(str(name) + " failed!")
