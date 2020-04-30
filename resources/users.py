import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash

users = Blueprint( "users", "users")

@users.route("/", methods=["GET"])
def test_user_route():
	return "user route working"

@users.route("/register", methods=["POST"])
def register_user():
	payload = request.get_json()
	payload["email"] = payload["email"].lower()
	payload["username"] = payload["username"].lower()

	try:
		models.User.get(models.User.email == payload["email"])
		return jsonify(
			data = {},
			message = f"Account with e-mail {payload['email']} already exists",
			status = 401
		), 401

	except models.DoesNotExist:
		try:
			models.User.get(models.User.username == payload["username"])
			return jsonify(
				data = {},
				message = f"Username {payload['username']} already taken",
				status = 401
			), 401

		except models.DoesNotExist:
			hashed_password = generate_password_hash(payload["password"])
			new_user = models.User.create(
				username = payload["username"],
				email = payload["email"],
				password = hashed_password
			)

			new_user_dict = model_to_dict(new_user)

			return jsonify(
				data = new_user_dict,
				message = f"Successfully registered {new_user_dict['username']}",
				status = 201
			), 201