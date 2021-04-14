from bson.objectid import ObjectId
from models import Game

def get_game_by_id(db, game_id):
    return db.games.find_one({"_id": ObjectId(game_id)})

def create_new_game(db):
    game = Game().to_dict()
    return db.games.insert_one(game)

def update_game(db, game):
    db.games.update_one({"_id": ObjectId(game["_id"])}, {"$set": {"dice": game["dice"], "form": game["form"], "roll_count": game["roll_count"], "announcement": game["announcement"]}}, upsert=False)

def restart_game_by_id(db, game_id):
    game = Game().to_dict()
    db.games.update_one({"_id": ObjectId(game_id)}, {"$set": {"dice": game["dice"], "form": game["form"], "roll_count": game["roll_count"], "announcement": game["announcement"]}}, upsert=False)
    return db.games.find_one({"_id": ObjectId(game_id)})

def game_exists_by_id(db, game_id):
    return db.games.find_one({"_id" : ObjectId(game_id)}) is not None