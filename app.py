from flask import Flask, render_template, jsonify, session, redirect, url_for
from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from models import Game
import os, sys, random

# database
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    MONGO_URI = "mongodb://localhost:27017/jamb"
client = MongoClient(MONGO_URI)
db = client.jamb

#flask app
app = Flask(__name__)
app.secret_key = "tanji ključ"
app.config["MONGO_URI"] = MONGO_URI


# default route
@app.route("/")
def index():
    try:
        # initialize game id
        game_id = ""
        # check if game id is not in session
        if "game_id" not in session:
            # if game id is not in session start new game
            game = Game()
            # save game to database and get game id
            game_id = str(db.games.insert_one(game.to_dict()).inserted_id)
            # put game id into session storage
            session["game_id"] = game_id
        # redirect to game view and start playing
        return redirect(url_for("game", game_id = session["game_id"]))
    except:
        # if an exception ocurred return error message
        return jsonify({"error": "Exception has ocurred"})


# game view route
@app.route("/game/<game_id>")
def game(game_id):
    try:
        # if game_id parameter is missing or invalid redirect to index
        if game_id is None or game_id == "":
            return redirect(url_for("index"))
        # if game id is not in session add it
        if "game_id" not in session:
            session["game_id"] = game_id
        # get game from database by game id
        game = db.games.find_one({"_id": ObjectId(game_id)})
        # if no game is present with id reset session storage and redirect to index
        if game is None:
            session.pop("game_id")
            return redirect(url_for("index"))
        # if game is valid render view with game parameter
        return render_template("game.html", game=game)
    except:
        # if an exception ocurred return error message
        return jsonify({"error": "Exception has ocurred"})


# route for rolling dice
@app.route("/game/roll", methods=["PUT"])
def roll():
    try:
        # check if game id in session
        if "game_id" not in session:
            return jsonify({"error": "No game is in session"})
        # get game_id from session
        game_id = session["game_id"]
        # get game from database by game id
        game = db.games.find_one({"_id": ObjectId(game_id)})
        # if game is invalid reset storage and redirect to index
        if game is None:
            session.pop("game_id")
            return redirect(url_for("index"))
        # get new dice values
        for dice in game["dice"]:
            dice["value"] = random.randint(1, 6)
        # update current game
        db.games.update_one({"_id": ObjectId(game_id)}, {"$set": {"dice": game["dice"]}}, upsert=False)
        # return dice values
        return jsonify({"message": [game["dice"]]})
    except:
        # if an exception ocurred return error message
        return jsonify({"error": "Exception has ocurred"})


if __name__ == "__main__":
    app.run(debug=True)
