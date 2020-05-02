from flask_login import current_user
from functools import wraps

# requires logged in account to be a publisher

def publishers_only(func):
	@wraps(func)
	def decorate_view(*args, **kwargs):
		if current_user.role == "publisher":
			return func(*args, **kwargs)
		else:
			return jsonify(
				data = {},
				message = "Action only available to registered publishers",
				status = 401
			), 401

# requires logged in account to be a user

def users_only(func):
	@wraps(func)
	def decorate_view(*args, **kwargs):
		if current_user.role == "user":
			return func(*args, **kwargs)
		else:
			return jsonify(
				data = {},
				message = "Action only available to registered users",
				status = 401
			), 401