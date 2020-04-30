import models
from flask import Blueprint

users = Blueprint( "users", "users")

@users.route("/", methods=["get"])
def test_user_route():
	return "user route working"