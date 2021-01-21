from bson.objectid import ObjectId
from models import Game

def get_game_by_id(db, game_id):
    return db.games.find_one({"_id": ObjectId(game_id)})

def new_game(db):
    game = Game()
    return db.games.insert_one(game.to_dict()).inserted_id

def update_game(db, game):
    db.games.update_one({"_id": ObjectId(game.id)}, {"$set": {"columns": game["columns"], "roll_count": game["roll_count"], "announcement": game["announcement"]}}, upsert=False)
