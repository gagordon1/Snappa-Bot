import requests

# BASE_URL = "https://snappa-bot-groupme-server.herokuapp.com" #DEPLOYED
# BASE_URL = "http://127.0.0.1:5000" #TEST


INITIAL_ELO = 1500
INITIAL_WINS = 0
INITIAL_LOSSES = 0

def add_player(player):
    print("Adding player", player)
    data = {
        "name" : player,
        "initial_elo" : INITIAL_ELO,
        "initial_wins" : INITIAL_WINS,
        "initial_losses" : INITIAL_LOSSES
        }
    response = requests.post(BASE_URL + "/players", json = data)
    return response.text

def log_game(player_1, player_2, player_3, player_4, score_1, score_2):
    print("Logging game", player_1, player_2, player_3, player_4, score_1, score_2)
    data = {
        "player1" : player_1,
        "player2" : player_2,
        "player3" : player_3,
        "player4" : player_4,
        "team_1_score" : score_1,
        "team_2_score" : score_2
        }
    response = requests.post(BASE_URL + "/games", json = data)
    return response.text

def get_leaderboard(n):
    response = requests.get(BASE_URL + "/leaderboard", json = {"n": n})
    return response.text

def get_player_data(player):

    response = requests.get(BASE_URL + "/players", json = {"name" : player})
    return response.text

def get_random_message():
    response = requests.get(BASE_URL + "/message")
    return response.text

def test_1():
    names = ["p1", "p2", "p3", "p4"]
    #add four players
    for name in names:

        response = add_player(name)

        print("Response", response)

    #add a bad player

    response = add_player("")
    print("Response", response)

    response = add_player("p1")
    print("Response", response)

    response = log_game(*names, 7,5)
    print("Response", response)

    #add a bad game
    names2 = names[:]
    names2[0] = "p11"
    response = log_game(*names2, 7,5)
    print("Response", response)

    n = 3
    response = get_leaderboard(n)
    print("Response\n", response)

    response = log_game(*names, 3,7)
    print("Response", response)

    response = get_player_data("p1")
    print("Response", response)

    n = 4
    response = get_leaderboard(n)
    print("Response\n", response)

    response = get_random_message()
    print("Response", response)


if __name__ == '__main__':
    test_1()
