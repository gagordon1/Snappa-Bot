#READ groupme import json
from flask import Flask, request, redirect, g, render_template, jsonify


PORT = 8080

app = Flask(__name__)


@ app.route("/", methods=["GET"])
def home():
    return requst.text

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
