from flask_login import current_user

# requires logged in user to be a publisher

def publishers_only(func):
	if current_user.role == "publisher":
		return func()
	else:
		return jsonify(
			data = {},
			message = "Action only available to registered publishers",
			status = 401
		), 401