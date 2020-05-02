import models
from decorators import publishers_only, users_only
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

games = Blueprint("games", "games")

# create route

@games.route("/", methods=["POST"])
@login_required
@publishers_only
def add_game():
	payload = request.get_json()
	new_game = models.Game.create(
		title = payload["title"],
		min_players = payload["min_players"],
		max_players = payload["max_players"],
		publisher = current_user.id)
	new_game_dict = model_to_dict(new_game)
	for i in payload["genres"]:
		try:
			genre_to_add = models.Genre.get(models.Genre.name == i)
		except models.DoesNotExist:
			genre_to_add = models.Genre.create(
				name = i,
				description = "")
		genre_to_add_dict = model_to_dict(genre_to_add)
		models.GameGenreRelationship.create(
			game = new_game_dict["id"],
			genre = genre_to_add_dict["id"])
	new_game_dict["publisher"].pop("password")
	return jsonify(
		data = new_game_dict,
		message = "Game added",
		status = 201
	), 201	

# index route

@games.route("/", methods=["GET"])
def games_index():
	query_results = models.Game.select()
	all_games = [model_to_dict(game_model) for game_model in query_results]
	for game_dict in all_games:
		genre_query = (models.GameGenreRelationship
			.select()
			.where(models.GameGenreRelationship.game_id == game_dict["id"]))
		genre_list = ([model_to_dict(q)["genre"] for q in genre_query])
		game_dict["genres"] = genre_list
		game_dict["publisher"].pop("password")
	return jsonify(
		data = all_games,
		message = f"Returned {len(all_games)} games",
		status = 200
	), 200

# delete route

@games.route("/<id>", methods=["DELETE"])
@login_required
def delete_game(id):
	game_to_delete = models.Game.get_by_id(id)
	if game_to_delete.publisher.id == current_user.id:
		# models.GameGenreRelationship.delete().where(models.GameGenreRelationship.game.id == game_to_delete.id)
		game_to_delete.delete_instance()
		return jsonify(
			data = {},
			message = "Game Deleted",
			status = 200
		), 200
	else:
		return jsonify(
			data = {},
			message = "Forbidden. Games can only be deleted by their publisher.",
			status = 403
		), 403

# update route

@games.route("/<id>", methods=["PUT"])
@login_required
def update_game(id):
	game_to_update = models.Game.get_by_id(id)
	if game_to_update.publisher.id == current_user.id:
		payload = request.get_json()
		genre_query = (models.GameGenreRelationship
			.select()
			.where(models.GameGenreRelationship.game_id == game_to_update.id))
		relationship_list = ([model_to_dict(q) for q in genre_query])
		existing_genres = [relationship["genre"]["name"] for relationship in relationship_list]
		for relationship in relationship_list:
			if relationship["genre"]["name"] not in payload["genres"]:
				models.GameGenreRelationship.get_by_id(relationship["id"]).delete_instance()
		for i in payload["genres"]:
			if i not in existing_genres:
				try:
					genre_to_add = models.Genre.get(models.Genre.name == i)
				except models.DoesNotExist:
					genre_to_add = models.Genre.create(
						name = i,
						description = "")
				# genre_to_add_dict = model_to_dict(genre_to_add)
				models.GameGenreRelationship.create(
					game = game_to_update.id,
					genre = genre_to_add.id)
		game_to_update.title = payload["title"]
		game_to_update.min_players = payload["min_players"]
		game_to_update.max_players = payload["max_players"]
		game_to_update.save()
		genre_query = (models.GameGenreRelationship
			.select()
			.where(models.GameGenreRelationship.game_id == game_to_update.id))
		game_dict = model_to_dict(game_to_update)
		genre_list = [model_to_dict(q)["genre"] for q in genre_query]
		game_dict["genres"] = genre_list
		game_dict["publisher"].pop("password")
		return jsonify(
			data = game_dict,
			message = f"{game_dict['title']} updated",
			status = 200
		), 200

	else:
		return jsonify(
			data = {},
			message = "Forbidden. Games can only be edited by their publisher.",
			status = 403
		), 403

# add favorite route

@games.route("/favorite/<id>", methods=["POST"])
@login_required
@users_only
def add_favorite(id):
	models.Favorite.create(
		user = current_user.id,
		game = id)
	return jsonify(
		data = {},
		message = "Favorite added",
		status = 200
	), 200


# test route

@games.route("/test")
@users_only
def test():
	print(current_user.role)
	return "Games route working"