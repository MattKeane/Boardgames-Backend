import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required
from decorators import publishers_only


genres = Blueprint("genres", "genres")

@genres.route("/test", methods=["GET"])
def genres_test():
	return "Genres route connected and functioning"

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