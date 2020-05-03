import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user

accounts = Blueprint( "accounts", "accounts")

# test route

@accounts.route("/", methods=["GET"])
def test_user_route():
	return jsonify(
		data = {},
		message = "Route is working",
		status = 200
	), 200

# registration route

@accounts.route("/register", methods=["POST"])
def register_user():
	payload = request.get_json()
	payload["email"] = payload["email"].lower()
	payload["username"] = payload["username"].lower()

	try:
		models.Account.get(models.Account.email == payload["email"])
		return jsonify(
			data = {},
			message = f"Account with e-mail {payload['email']} already exists",
			status = 401
		), 401

	except models.DoesNotExist:
		try:
			models.Account.get(models.Account.username == payload["username"])
			return jsonify(
				data = {},
				message = f"Username {payload['username']} already taken",
				status = 401
			), 401

		except models.DoesNotExist:
			hashed_password = generate_password_hash(payload["password"])
			new_user = models.Account.create(
				username = payload["username"],
				email = payload["email"],
				password = hashed_password,
				role = payload["role"]
			)

			login_user(new_user)

			new_user_dict = model_to_dict(new_user)

			new_user_dict.pop("password")

			return jsonify(
				data = new_user_dict,
				message = f"Successfully registered {new_user_dict['username']}",
				status = 201
			), 201

# login route

@accounts.route("/login", methods=["POST"])
def login():
	payload = request.get_json()
	payload["email"] = payload["email"].lower()
	try:
		user = models.Account.get(models.Account.email == payload["email"])
		user_dict = model_to_dict(user)
		password_is_correct = check_password_hash(user_dict["password"], payload["password"])
		if password_is_correct:
			login_user(user)
			user_dict.pop("password")
			return jsonify(
				data = user_dict,
				message = f"{user_dict['username']} signed in.",
				status = 200
			), 200
		else:
			print("Invalid password")
			return jsonify(
				data = {},
				message = "Invalid e-mail or password",
				status = 401
			), 401
	except models.DoesNotExist:
		print("Invalid e-mail")
		return jsonify(
			data = {},
			message = "Invalid e-mail or password",
			status = 401
		), 401

# check logged in user route

@accounts.route("/logged_in_user", methods=["GET"])
def get_logged_in_user():
	if not current_user.is_authenticated:
		return jsonify(
			data = {},
			message = "No user is currently logged in",
			status = 401
		), 401

	else:
		user_dict = model_to_dict(current_user)
		user_dict.pop("password")
		return jsonify(
			data = user_dict,
			message = f"{user_dict['username']} currently logged in.",
			status = 200
		), 200

# log out route

@accounts.route("/logout", methods=["GET"])
def logout():
	logout_user()
	return jsonify(
		data={},
		message="Logged out.",
		status=200
	), 200

# Get favorites wrote

@accounts.route("/favorites/<id>", methods=["GET"])
def get_favorites(id):
	favorites_query = models.Favorite.select().where(models.Favorite.user_id == id)
	users_favorites = [model_to_dict(i)["game"] for i in favorites_query]
	for i in users_favorites:
		i["publisher"].pop("password")
	return jsonify(
		data = users_favorites,
		message = f"Returned {len(users_favorites)} favorite games",
		status = 200
	), 200




