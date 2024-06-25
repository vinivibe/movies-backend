from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app):
    mongo.init_app(app)

def get_movies_collection():
    return mongo.db.movies

def get_favorites_collection():
    return mongo.db.favorites

def get_watched_collection():
    return mongo.db.watched
