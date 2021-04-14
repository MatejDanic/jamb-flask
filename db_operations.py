from bson import ObjectId
from models import Game

def find_game_by_id(db, game_id):
    return db.games.find_one({"_id": ObjectId(game_id)})

def create_new_game(db):
    game = Game().to_dict()
    inserted_id = db.games.insert_one(game).inserted_id
    return db.games.find_one({"_id": inserted_id})

def update_game(db, game):
    db.games.update_one({"_id": ObjectId(game["_id"])}, {"$set": {"dice": game["dice"], "form": game["form"], "roll_count": game["roll_count"], "announcement": game["announcement"]}}, upsert=False)

def restart_game_by_id(db, game_id):
    game = Game().to_dict()
    db.games.update_one({"_id": ObjectId(game_id)}, {"$set": {"dice": game["dice"], "form": game["form"], "roll_count": game["roll_count"], "announcement": game["announcement"]}}, upsert=False)
    return db.games.find_one({"_id": ObjectId(game_id)})

def remove_game_by_id(db, game_id):
    db.games.remove({"_id": ObjectId(game_id)})

def game_exists_by_id(db, game_id):
    return db.games.find_one({"_id" : ObjectId(game_id)}) is not None