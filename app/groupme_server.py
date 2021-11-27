#READ groupme import json
from flask import Flask, request, redirect, g, render_template, jsonify
import json
import requests
from Databases.DictionaryDatabase import DictionaryDatabase
from Databases.GoogleSheetsDatabase import GoogleSheetsDatabase
from SnappaLeaderboard import SnappaLeaderboard
from HelperFunctions.parse_text import parse_text
from HelperFunctions.execute_action import execute_action
from HelperFunctions.send_to_groupme import send_to_groupme

import sys


PORT = 8080

app = Flask(__name__)

GROUPME_ID = 163797812604437644 #TEST GROUP
BOT_ID = "d9ce63918a5ba0a22008fa71dc"
BASE_POST_URL = "https://api.groupme.com/v3/bots/post"

LEADERBOARD_SIZE = 20
INITIAL_ELO = 1500
INITIAL_WINS = 0
INITIAL_LOSSES = 0

# db = DictionaryDatabase()
db = GoogleSheetsDatabase()
slb = SnappaLeaderboard(db)


"""
#POST requests from groupme appear like:
{
    "attachments":[],
    "avatar_url":"https://i.groupme.com/750x744.jpeg.0f268692d87a4254a35623c95efa73ba",
    "created_at":1637978126,
    "group_id":"83775365",
    "id":"163797812604437644",
    "name":"Garrett Gordon",
    "sender_id":"38446275",
    "sender_type":"user",
    "source_guid":"C0227DA0-438D-4A39-ABF0-36EE77222B24",
    "system":false,
    "text":"hi",
    "user_id":"38446275"
}
"""
@ app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        return "WELCOME TO SNAPPA BOT BITCH"
    elif request.method == "POST":
        data = json.loads(request.data.decode("UTF-8"))
        text = data["text"]
        name = data["name"]
        action, parameters = parse_text(text, LEADERBOARD_SIZE,
                INITIAL_ELO, INITIAL_WINS, INITIAL_LOSSES, name)
        print(action, parameters)
        respond, response = execute_action(action, parameters)
        print(respond, response)
        if respond:
            send_to_groupme(BASE_POST_URL, BOT_ID, response)
        return response
    else:
        return "WELCOME TO SNAPPA BOT"

"""
POST
    json data
    name : str
    initial_elo : int
    initial_wins : int
    initial_losses : int

    Response:
    "Player {name} successfully added!" | "Player {name}'s name is too long"
    | Player's name cannot be empty!

GET
    name : str

    Response:
    Tabulated string of player data | "Player data could not be accessed!"

"""
@ app.route("/players", methods=["POST", "GET"])
def players():
    response = ""
    if request.method == "POST":
        data = request.json
        try:
            slb.add_player(
                data["name"],
                data["initial_elo"],
                data["initial_wins"],
                data["initial_losses"]
            )
            return "Player {} successfully added!".format(data["name"])
        except Exception as e:
            return str(e)
        return "Error adding player!"

    elif request.method == "GET":
        data = request.json
        try:
            response = slb.get_player_data(data["name"])
            return response
        except Exception as e:
            return str(e)
        return "Player data could not be accessed!"

    else:
        return "Only POST and GET requests are supported!"




"""
POST
    json data
    player1 : str
    player2 : str
    player3 : str
    player4 : str
    team_1_score : int
    team_2_score : int

    Response:
    Table of posted update string | "Game could not be logged!"
    | "Player {name} does not exist in the database!"
    | Game successfully logged!
"""
@ app.route("/games", methods=["POST"])
def games():
    if request.method == "POST":
        data = request.json
        try:
            response = slb.log_score(
                data["player1"],
                data["player2"],
                data["player3"],
                data["player4"],
                data["team_1_score"],
                data["team_2_score"],
            )
            return response
        except Exception as e:
            return str(e)

        return "Game could not be logged!"
    else:
        return "Only POST requests are supported!"

"""
GET
    json data
    n: int

    Response:
    Leaderboard String | "Database could not be accessed!"
"""
@ app.route("/leaderboard", methods=["GET"])
def leaderboard():
    if request.method == "GET":
        data = request.json
        n = data["n"]
        try:
            response = slb.get_leaderboard(n)
            return response
        except Exception as e:
            return str(e)
        return "Database could not be accessed!"

    else:
        return "Only GET requests are supported!"

"""
GET
    Response:
    Random message
"""
@ app.route("/message", methods=["GET"])
def message():
    if request.method == "GET":
        try:
            response = slb.generate_message()
            return response
        except:
            return "Message could not be generated!"

    else:
        return "Only GET requests are supported!"

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
