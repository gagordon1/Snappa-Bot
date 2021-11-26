import json
from flask import Flask, request, redirect, g, render_template, jsonify
import requests
import uuid

PORT = 8080

app = Flask(__name__)

@ app.route("/", methods=["GET"])
def home():
    return "WELCOME TO SNAPPA BOT BITCH"

"""
POST
    name : str
    initial_elo : int
    initial_wins : int
    initial_losses : int

    Response:
    "Player {name} successfully added!" | "Player {name}'s name is too long"
    | Player's name cannot be empty!
"""
@ app.route("/players", methods=["POST", "GET"])
def players():
    pass


"""
POST
    player1 : str
    player2 : str
    player3 : str
    player4 : str
    winner_score : int
    loser_score : int

    Response:
    Table of posted update string | "Game could not be logged!"
    | "Player {name} does not exist in the database!"
    | Game successfully logged!
"""
@ app.route("/games", methods=["POST"])
def games():
    pass

"""
GET
    Response:
    Leaderboard String | "Database could not be accessed!"
"""
@ app.route("/leaderboard", methods=["GET"])
def leaderboard():
    pass


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
