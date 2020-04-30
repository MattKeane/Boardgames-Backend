# modules
from flask import Flask 
from flask_login import LoginManager

# models
import models

# blueprints
from resources.accounts import accounts
from resources.games import games

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
		user = models.Account.get_by_id(user_id)
		return user
	except models.DoesNotExist:
		return none

@app.route("/")
def test():
	return "server is running"

# define routes
app.register_blueprint(accounts, url_prefix = "/api/v1/accounts")
app.register_blueprint(games, url_prefix = "/api/v1/games")

if __name__ == "__main__":
	models.initialize()
	app.run(debug=DEBUG, port=PORT)