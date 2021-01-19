from flask import Flask, render_template, jsonify, session, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from models import Game
import os, sys, random

MONGODB_URI = os.environ.get('MONGODB_URI')
if not MONGODB_URI:
    MONGODB_URI = "mongodb://localhost:27017/jamb"

app = Flask(__name__)

app.secret_key = "tanji ključ"
app.config['MONGODB_URI'] = MONGODB_URI

try :
    client = MongoClient(MONGODB_URI)
except:
    print("Exception se dogodio")
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


if __name__ == "__main__":
    app.run(debug=True)
