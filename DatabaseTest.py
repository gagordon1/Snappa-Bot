from time import time
from DictionaryDatabase import DictionaryDatabase
from GoogleSheetsDatabase import GoogleSheetsDatabase

def addPlayerTest1(db):
    response = db.add_player("Garrett", 1500, 0 , 0)
    if response != "Player Garrett successfully added!":
        return False

    #Try to add the same player twice
    response = db.add_player("Garrett", 1500, 0, 0)
    if response != "Player already exists in the database!":
        return False

    response = db.add_player("Noah", 1500, 0 ,0)
    if response != "Player Noah successfully added!":
        return False

    response = db.get_player_data("Garrett")
    if response != [1500, 0 ,0]:
        return False

    response = db.get_player_data("Noah")
    if response != [1500, 0 ,0]:
        return False

    return True


def updatePlayerDataTest1(db):
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

def getLeaderboardTest1(db):
    expected = [["Andrei", 1502, 1,1], ["Garrett", 1502,1,1], ["Noah", 1498,1,1], ["Sebastian", 1498,1,1]]
    result = db.get_leaderboard()
    for l in expected:
        if l not in result:
            return False
    return True


def logGameTest1(db):
    db.add_player("Andrei", 1500, 0, 0)
    db.add_player("Sebastian", 1500, 0, 0)

    t = int(time())
    game = [t, "Garrett", "Andrei", "Noah", "Sebastian",7,2]
    response = db.log_game(*game)
    if response != "Game successfully logged!":
        return False

    response = db.get_player_games("Garrett")
    if response != [game]:
        return False

    response = db.log_game(t, "Garret", "Andrei", "Noah", "Sebastian",7,2)
    if response != "Player Garret does not exist in the database!":
        return False

    t = int(time())
    game2 = [t, "Garrett", "Noah", "Andrei", "Sebastian",3,7]
    response = db.log_game(*game2)
    if response != "Game successfully logged!":
        return False

    response = db.get_player_games("Garrett")
    for g in game, game2:
        if g not in response:
            return False

    return True


if __name__ == '__main__':
    # db = DictionaryDatabase()
    db = GoogleSheetsDatabase(test = True)
    for name, test in [
        ["Add Player Test 1", addPlayerTest1],
        ["Log Game Test 1", logGameTest1],
        ["Update Player Data Test 1", updatePlayerDataTest1],
        ["Get Leaderboard Test 1", getLeaderboardTest1]
    ]:
        if test(db):
            print(name + " passed!")
        else:
            print(name + " failed!")
