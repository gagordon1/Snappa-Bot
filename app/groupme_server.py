#READ groupme import json
from flask import Flask, request, redirect, g, render_template, jsonify
import json


PORT = 8080

app = Flask(__name__)


@ app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        return "WELCOME TO SNAPPA BOT BITCH"
    elif request.method == "POST":
        data = request.data.decode("UTF-8")
        print(type(data))
        text = data["text"]
        author = data["name"]

        return request.data
    else:
        return "WELCOME TO SNAPPA BOT"

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
