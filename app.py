from flask import Flask, render_template, jsonify, session, redirect, url_for
from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from models import Game
import os, sys, random

app = Flask(__name__)

app.secret_key = "tanji ključ"

client = MongoClient("mongodb+srv://dbUser:SWDAGlSdPAbgrgEC@cluster0.m0vzw.mongodb.net/jamb?retryWrites=true&w=majority")

try:
    print(client.server_info())
    sys.stdout.flush()
except errors.ServerSelectionTimeoutError as err:
    print(err)
    sys.stdout.flush()

db = client.jamb




@app.route("/")
def index():
    try:
        game_id = ""
        if "game_id" not in session:
            game = Game()
            game_id = str(db.games.insert_one(game.to_dict()).inserted_id)
            session["game_id"] = game_id
        return redirect(url_for("game", game_id = session["game_id"]))
    except:
        return jsonify({"error": "exception"})


@app.route("/game/<game_id>")
def game(game_id):
    try:
        if not game_id:
            return render_template("game.html")
        if "game_id" not in session:
            session["game_id"] = game_id
        game = db.games.find_one({"_id": ObjectId(game_id)})
        if game is None:
            session.pop("game_id")
            return redirect(url_for("index"))
        return render_template("game.html", game=game)
    except:
        return jsonify({"error": "exception"})


@app.route("/game/roll", methods=["PUT"])
def roll():
    try:
        if "game_id" not in session:
            return jsonify({"error": "no game id in session"})
        game_id = session["game_id"]
        game = db.games.find_one({"_id": ObjectId(game_id)})
        if game is None:
            session.pop("game_id")
            return jsonify({"error": "no game with dis id"})
        for dice in game["dice"]:
            dice["value"] = random.randint(1, 6)
        db.games.update_one({'_id': ObjectId(game_id)}, {'$set': {"dice": game["dice"]}}, upsert=False)
        return jsonify({"message": [game["dice"]]})
    except:
        return jsonify({"error": "exception"})

@app.route("/test")
def test():
    return "Test"


if __name__ == "__main__":
    app.run(debug=True)
