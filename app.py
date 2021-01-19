from flask import Flask, render_template, jsonify, session, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from models import Game
import os, random


app = Flask(__name__)
app.secret_key = "tanji ključ"

client = MongoClient(os.environ.get("MONGODB_URI", "mongodb+srv://dbUser:SWDAGlSdPAbgrgEC@cluster0.m0vzw.mongodb.net/jamb?retryWrites=true&w=majority"), connect=False, ssl=True)

db = client.jamb


@app.route("/")
def index():
    game_id = ""
    if "game_id" not in session:
        game = Game()
        game_id = str(db.games.insert_one(game.to_dict()).inserted_id)
        session["game_id"] = game_id
    return redirect(url_for("game", game_id = session["game_id"]))


@app.route("/game/<game_id>")
def game(game_id):
    game = db.games.find_one({"_id": ObjectId(game_id)})
    if game is None:
        session.pop("game_id")
        return redirect(url_for("index"))
    return render_template("game.html", game=game)


@app.route("/game/roll", methods=["PUT"])
def roll():
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


if __name__ == "__main__":
    app.run(debug=True)
