import pygsheets
from GoogleSheetsDatabase import GoogleSheetsDatabase
from time import time

SERVICE_FILE = 'google_keys/spartan-matter-323500-b7144290e762.json'
SPREADSHEET_NAME = "Snappa Database"
PLAYER_SHEET_INDEX = 2
GAME_SHEET_INDEX = 3
START_OF_DATA = "B3"

def get_worksheet(sheet_index):
    gc = pygsheets.authorize(service_file=SERVICE_FILE)
    sh = gc.open(SPREADSHEET_NAME)
    wks = sh.worksheets()[sheet_index]
    return wks


def addPlayerTest1():
    wks = get_worksheet(PLAYER_SHEET_INDEX)
    db = GoogleSheetsDatabase(PLAYER_SHEET_INDEX, GAME_SHEET_INDEX)
    response = db.add_player("Garrett")
    if response != "Player Garrett successfully added!":
        return False
    test_row_number = 3
    row = wks.get_row(test_row_number)
    if row[1:5] != ['Garrett', '1500', '0', '0']:
        return False

    #Try to add the same player twice
    response = db.add_player("Garrett")
    if response != "Player already exists in the database!":
        return False

    response = db.add_player("Noah")
    if response != "Player Noah successfully added!":
        return False
    test_row_number_2 = 4
    row = wks.get_row(test_row_number)
    row2 = wks.get_row(test_row_number_2)
    if row[1:5] != ['Garrett', '1500', '0', '0'] or row2[1:5] != ['Noah', '1500', '0', '0']:
        return False

    return True


def updatePlayerDataTest1():
    wks = get_worksheet(GAME_SHEET_INDEX)
    db = GoogleSheetsDatabase(PLAYER_SHEET_INDEX, GAME_SHEET_INDEX)
    response = db.updatePlayerData("Garrett", 1502, 1, 1)
    if response != "Player data successfully updated!":
        return False

    response = db.updatePlayerData("Garret", 1502, 1, 1)

    if response != "Player Garret does not exist in the database!":
        return False

    response = db.updatePlayerData("Andrei", 1502, 1, 1)
    response = db.updatePlayerData("Noah", 1498, 1, 1)
    response = db.updatePlayerData("Sebastian", 1498, 1, 1)

    out = db.get_player_data("Garrett")
    if [1502,1,1] != out:
        return False
    if [1502,1,1] != db.get_player_data("Andrei"):
        return False
    if [1498,1,1] != db.get_player_data("Noah"):
        return False
    if [1498,1,1] != db.get_player_data("Sebastian"):
        return False

    return True

def getLeaderboardTest1():
    wks = get_worksheet(PLAYER_SHEET_INDEX)
    db = GoogleSheetsDatabase(PLAYER_SHEET_INDEX, GAME_SHEET_INDEX)
    expected = [["Andrei", 1502, 1,1], ["Garrett", 1502,1,1], ["Noah", 1498,1,1], ["Sebastian", 1498,1,1]]
    result = db.get_leaderboard()
    print(result)
    for l in expected:
        if l not in result:
            return False
    return True


def logGameTest1():
    wks = get_worksheet(GAME_SHEET_INDEX)
    db = GoogleSheetsDatabase(PLAYER_SHEET_INDEX, GAME_SHEET_INDEX)
    db.add_player("Andrei")
    db.add_player("Sebastian")

    t = int(time())
    response = db.log_game(t, "Garrett", "Andrei", "Noah", "Sebastian",7,2)
    if response != "Game successfully logged!":
        return False

    response = db.log_game(t, "Garret", "Andrei", "Noah", "Sebastian",7,2)
    if response != "Player Garret does not exist in the database!":
        return False

    test_row_number = 3
    row = wks.get_row(test_row_number)
    if row[1:8] != [str(t), "Garrett", "Andrei", "Noah", "Sebastian", "7", "2"]:
        return False


    t = int(time())
    response = db.log_game(t, "Garrett", "Andrei", "Noah", "Sebastian",3,7)
    if response != "Game successfully logged!":
        return False

    test_row_number = 4
    row = wks.get_row(test_row_number)
    if row[1:8] != [str(t), "Garrett", "Andrei", "Noah", "Sebastian", "3", "7"]:
        return False
    return True



def initialize_game_log():
    wks = get_worksheet(GAME_SHEET_INDEX)
    wks.clear(start = START_OF_DATA)



def initialize_player_sheet():
    wks = get_worksheet(PLAYER_SHEET_INDEX)
    wks.clear(start = START_OF_DATA)


if __name__ == '__main__':
    initialize_game_log()
    initialize_player_sheet()
    for name, test in [
        ["Add Player Test 1", addPlayerTest1],
        ["Log Game Test 1", logGameTest1],
        ["Update Player Data Test 1", updatePlayerDataTest1],
        ["Get Leaderboard Test 1", getLeaderboardTest1]
    ]:
        if test():
            print(name + " passed!")
        else:
            print(name + " failed!")
    initialize_game_log()
    initialize_player_sheet()
