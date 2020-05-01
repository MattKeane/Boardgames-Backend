from flask_login import current_user, login_required
from flask import jsonify

# requires logged in user to be a publisher

# @login_required
def publishers_only(func):
	def decorated_view(*args, **kwargs):
		if current_user.role == "publisher":
			return func(*args, **kwargs)
		else:
			return jsonify(
				data = {},
				message = "Action only available to registered publishers",
				status = 401
			), 401
	return decorated_view