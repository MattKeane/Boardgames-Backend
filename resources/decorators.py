from flask_login import current_user
from functools import wraps

# requires logged in user to be a publisher

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