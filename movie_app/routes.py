from flask import Blueprint, request, jsonify
from movie_app.models import get_movies_collection, get_favorites_collection, get_watched_collection
from movie_app.schemas import movie_schema  # Importar o schema de validação
import requests
import os
from bson.objectid import ObjectId
from dotenv import load_dotenv


load_dotenv()

bp = Blueprint('routes', __name__)


api_key = os.getenv('OMDB_API_KEY')

@bp.route('/add_movie', methods=['POST'])
def add_movie():
    data = request.json
    errors = movie_schema.validate(data)  
    if errors:
        return jsonify(errors), 400  
    collection = get_movies_collection()
    collection.insert_one(data)
    return jsonify({"message": "Filme cadastrado com sucesso!"}), 201

@bp.route('/movies', methods=['GET'])
def get_movies():
    collection = get_movies_collection()
    movies = list(collection.find())
    for movie in movies:
        movie['_id'] = str(movie['_id'])
    return jsonify(movies), 200

@bp.route('/movie/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    collection = get_movies_collection()
    movie = collection.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        return jsonify({"error": "Filme não encontrado"}), 404
    movie['_id'] = str(movie['_id'])
    return jsonify(movie), 200

@bp.route('/favorite', methods=['POST'])
def favorite_movie():
    data = request.json
    collection = get_favorites_collection()
    collection.insert_one(data)
    return jsonify({"message": "Filme favoritado com sucesso!"}), 201

@bp.route('/unfavorite/<movie_id>', methods=['DELETE'])
def unfavorite_movie(movie_id):
    collection = get_favorites_collection()
    collection.delete_one({"_id": movie_id})
    return jsonify({"message": "Filme removido dos favoritos!"}), 200

@bp.route('/watched', methods=['POST'])
def watched_movie():
    data = request.json
    collection = get_watched_collection()
    collection.insert_one(data)
    return jsonify({"message": "Filme marcado como assistido com sucesso!"}), 201

@bp.route('/delete_movie/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movies_collection = get_movies_collection()
    favorites_collection = get_favorites_collection()
    watched_collection = get_watched_collection()

    movies_collection.delete_one({"_id": ObjectId(movie_id)})
    favorites_collection.delete_one({"_id": ObjectId(movie_id)})
    watched_collection.delete_one({"_id": ObjectId(movie_id)})
    
    return jsonify({"message": "Filme deletado com sucesso!"}), 200

@bp.route('/favorites', methods=['GET'])
def get_favorites():
    collection = get_favorites_collection()
    favorites = list(collection.find())
    for favorite in favorites:
        favorite['_id'] = str(favorite['_id'])
    return jsonify(favorites), 200

@bp.route('/watched', methods=['GET'])
def get_watched():
    collection = get_watched_collection()
    watched = list(collection.find())
    for movie in watched:
        movie['_id'] = str(movie['_id'])
    return jsonify(watched), 200

@bp.route('/external_movies', methods=['GET'])
def get_external_movies():
    response = requests.get(f'http://www.omdbapi.com/?t=batman&y=2022&apikey={api_key}&type=movie')
    return jsonify(response.json()), 200

@bp.route('/movie_details', methods=['GET'])
def get_movie_details():
    title = request.args.get('title')
    imdb_id = request.args.get('imdb_id')
    
    if title:
        response = requests.get(f'http://www.omdbapi.com/?t={title}&apikey={api_key}')
    elif imdb_id:
        response = requests.get(f'http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}')
    else:
        return jsonify({"error": "title or imdb_id parameter is required"}), 400
    
    return jsonify(response.json()), 200

@bp.route('/edit_movie/<movie_id>', methods=['PUT'])
def edit_movie(movie_id):
    data = request.json
    collection = get_movies_collection()
    movie = collection.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        return jsonify({"error": "Filme não encontrado"}), 404
    errors = movie_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    collection.update_one({"_id": ObjectId(movie_id)}, {"$set": data})
    return jsonify({"message": "Filme atualizado com sucesso!"}), 200
