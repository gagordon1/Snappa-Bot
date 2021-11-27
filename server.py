import json
from flask import Flask, request, redirect, g, render_template, jsonify
import requests
import uuid
from Databases.DictionaryDatabase import DictionaryDatabase
from SnappaLeaderboard import SnappaLeaderboard
import sys

PORT = 8080

app = Flask(__name__)

db = DictionaryDatabase()
slb = SnappaLeaderboard(db)


@ app.route("/", methods=["GET"])
def home():
    return "WELCOME TO SNAPPA BOT BITCH"

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
    pass


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
