import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required
from decorators import publishers_only


genres = Blueprint("genres", "genres")

# test route

@genres.route("/test", methods=["GET"])
def genres_test():
	return "Genres route connected and functioning"

# create route

@genres.route("/", methods=["POST"])
@login_required
@publishers_only
def add_genre():
	payload = request.get_json()
	try:
		models.Genre.get(models.Genre.name == payload["name"])
		return jsonify(
			data = {},
			message = f"Genre {payload['name']} already exists)",
			status = 401
		), 401
	except models.DoesNotExist:
		new_genre = models.Genre.create(
			name = payload["name"],
			description = payload["description"])
		new_genre_dict = model_to_dict(new_genre)
		return jsonify(
			data = new_genre_dict,
			message = f"Genre {payload['name']} created",
			status = 201
		), 201

# index route

@genres.route("/", methods=["GET"])
def genres_index():
	query_result = models.Genre.select()
	all_genres = [model_to_dict(genre_model) for genre_model in query_result]
	return jsonify(
		data = all_genres,
		message = f"Returned {len(all_genres)} genres",
		status = 200
	), 200
