import requests
API_URL = "https://snappa-bot-groupme-server.herokuapp.com"

def make_post_request(endpoint, data = None):
    try:
        response = requests.post(API_URL + endpoint, json = data)
        response = response.text
    except:
        response = "Error making request!"
    return response

def make_get_request(endpoint, data = None):
    try:
        if data != None:
            response = requests.get(API_URL + endpoint, json = data)
            response = response.text
        else:
            response = requests.get(API_URL + endpoint)
            response = response.text
    except:
        response = "Error making request!"
    return response

def execute_action(action, parameters):
    """Executes an action specified by a groupme message

    Parameters
    ----------
    action : str
        add player | log score | get leaderboard | get player data
        | get message | none | error
    parameters : list
        list of parameters that go with their associated action

    Returns
    -------
    tuple
        (Boolean, Message)
        First index True if bot should send a response in the group message,
        otherwise return the response message without sending

    """
    if action == "error":
        return True, "There was an error parsing the groupme command, make sure the command was formatted properly."
    elif action == "add player":
        data = {
            "name" : parameters[0],
            "initial_elo" : parameters[1],
            "initial_wins" : parameters[2],
            "initial_losses" : parameters[3]
        }
        response = make_post_request("/players", data = data)
        return True, response

    elif action == "load members":
        response = make_get_request("/loadMembers")
        return True, response

    elif action == "log score":
        data = {
            "player1" : parameters[0],
            "player2" : parameters[1],
            "player3" : parameters[2],
            "player4" : parameters[3],
            "team_1_score" : parameters[4],
            "team_2_score" : parameters[5],
        }
        response = make_post_request("/games", data = data)
        return True, response

    elif action == "get leaderboard":
        data = {
            "n" : parameters[0]
        }
        response = make_get_request("/leaderboard", data = data)
        return True, response

    elif action == "get player data":
        data = {
            "name" : parameters[0]
        }
        response = make_get_request("/players", data = data)
        return True, response

    elif action == "get message":
        response = make_get_request("/message")
        return True, response
    else:
        action = "none"
        return False, "Nothing to do"


if __name__ == '__main__':
    for name in ["Garrett", "Andrei", "Sebastian", "Noah"]:
        action = "add player"
        parameters = [name, 1500, 0, 0]
        respond, response = execute_action(action, parameters)
        print(response)

    action = "log score"
    parameters =["Garrett", "Noah", "Sebastian", "Andrei", 7, 2]
    respond, response = execute_action(action, parameters)
    print(response)

    action = "get leaderboard"
    parameters = [2]
    respond, response = execute_action(action, parameters)
    print(response)

    action = "get player data"
    parameters = ["Andrei"]
    respond, response = execute_action(action, parameters)
    print(response)

    action = "get message"
    parameters = []
    respond, response = execute_action(action, parameters)
    print(response)

    action = "none"
    parameters = []
    respond, response = execute_action(action, parameters)
    print(response)
