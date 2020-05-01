import models
from decorators import publishers_only
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

games = Blueprint("games", "games")

# create route

@games.route("/", methods=["POST"])
# @login_required
@publishers_only
def add_game():
	payload = request.get_json()
	new_game = models.Game.create(
		title = payload["title"],
		min_players = payload["min_players"],
		max_players = payload["max_players"],
		publisher = current_user.id)
	new_game_dict = model_to_dict(new_game)
	new_game_dict["publisher"].pop("password")
	return jsonify(
		data = new_game_dict,
		message = "Game added",
		status = 201
	), 201		
		




# test route

@games.route("/test")
def test():
	return "Games route working"