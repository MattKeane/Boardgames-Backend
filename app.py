# modules
from flask import Flask 
from flask_login import LoginManager

# models
import models

# blueprints
from resources.users import users

DEBUG=True
PORT=8000

app = Flask(__name__)

# user sessions
app.secret_key = "k877DAFi887&*hj98"
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
	try:
		print("Loading user:")
		user = models.User.get_by_id(user_id)
		return user
	except models.DoesNotExist:
		return none

@app.route("/")
def test():
	return "server is running"

# define routes
app.register_blueprint(users, url_prefix = "/api/v1/users")

if __name__ == "__main__":
	models.initialize()
	app.run(debug=DEBUG, port=PORT)