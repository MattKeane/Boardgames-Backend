import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

games = Blueprint("games", "games")

@games.route("/test")
def test():
	return "Games route working"