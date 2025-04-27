from .mongodb import get_database

db = get_database()

users_col = db["users"]
games_col = db["games"]
interactions_col = db["interactions"]

