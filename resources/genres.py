import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict


genres = Blueprint("genres", "genres")

@genres.route("/test", methods=["GET"])
def genres_test():
	return "Genres route connected and functioning"