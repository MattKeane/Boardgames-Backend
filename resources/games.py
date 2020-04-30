import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user

games = Blueprint("games", "games")

# create route

@games.route("/", methods=["POST"])
def add_game():
	if current_user.is_authenticated:
		payload = request.get_json()
		new_game = models.Game.create(
			title = payload["title"],
			min_players = payload["min_players"],
			max_players = payload["max_players"],
			publisher = payload["publisher"],
			added_by = current_user.id)
		new_game_dict = model_to_dict(new_game)
		return jsonify(
			data = new_game_dict,
			message = "Game added",
			status = 201
		), 201

	else:
		return jsonify(
			data = {},
			message = "User must be logged in to add a game",
			status = 401
		), 401


# test route

@games.route("/test")
def test():
	return "Games route working"