from flask import Flask, Response, request, render_template, redirect, url_for, jsonify, session
from pymongo import MongoClient, errors
import os, sys, random
import db_operations

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
        # check if game id is in session
        if "game_id" in session:
            # get game id from session
            game_id = session["game_id"]
            # check game id validity
            if game_id is None or game_id == "":
                # if game id is invalid clear the session storage
                session.pop("game_id")
        # if game id is not in session
        if "game_id" not in session:
            # save game to database and get game id
            game_id = db_operations.new_game(db)
            # put game id into session storage
            session["game_id"] = str(game_id)
        # redirect to game view and pass game id parameter
        return redirect(url_for("game", game_id=game_id))
    except Exception as error:
        # if an exception ocurred render view with error message
        return render_template("error.html", error=error)


# game view route
@app.route("/game/<game_id>")
def game(game_id):
    try:
        game = db_operations.get_game_by_id(db, game_id)
        # if game id is not already in session add it
        if "game_id" not in session:
            if not game_id == session["game_id"]:
                session["game_id"] = game_id
        # get game from database by game id
        # if no game with given id is retrieved
        if game is None:
            # clear session storage
            session.pop("game_id")
            # redirect to index to create a new game+
            return redirect(url_for("index"))
        # if game is successfully retrieved from database render game view
        return render_template('game.html', game={x: game[x] for x in game if not x == "_id"})
    except Exception as error:
        # if an exception ocurred render view with error message
        return render_template("error.html", error=error)


# route for rolling dice
@app.route("/game/<game_id>/roll", methods=["PUT"])
def roll(game_id):
    try:
        # get game from database by game id
        game = db_operations.get_game_by_id(db, game_id)
        dice_to_roll = request.data
        for dice in dice_to_roll:
            game["dice"][dice] = random.randint(1, 6)
        # update current game
        db_operations.update_game(db, game)
        # return dice values
        return Response(game["dice"], status=200)
    except Exception as error:
        # if an exception ocurred return error status
        return Response(error, status=500)


# route for restarting game
@app.route("/game/<game_id>/restart", methods=["PUT"])
def restart(game_id):
    try:
        # get game from database by game id
        game = db_operations.get_game_by_id(db, game_id)
        game["announcement"] = None
        game["roll_count"] = 0
        for column in game["columns"]:
            for box in game["boxes"]:
                box["value"] = 0
                box["filled"] = False
                box["available"] = False
        for dice in game["dice"]:
            dice["value"] = 6
        # update game
        db_operations.update_game(db, game)
        # return dice values
        return Response(game, status=200)
    except Exception as error:
        # if an exception ocurred return error status
        return Response(error, status=500)


if __name__ == "__main__":
    app.run(debug=True)
