# modules
import os
from flask import Flask, g, jsonify
from flask_login import LoginManager
from flask_cors import CORS
from dotenv import load_dotenv

# models
import models

# blueprints
from resources.accounts import accounts
from resources.games import games
from resources.genres import genres

load_dotenv()

SESSION_SECRET = os.getenv('SESSION_SECRET')
DEBUG	=	True
PORT = 8000

app = Flask(__name__)
app.config.update(
  SESSION_COOKIE_SECURE=True,
  SESSION_COOKIE_SAMESITE='None'
)

# user sessions
app.secret_key = SESSION_SECRET
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
	try:
		print("Loading user:")
		user = models.Account.get_by_id(user_id)
		print(user)
		return user
	except models.DoesNotExist:
		return None

@login_manager.unauthorized_handler
def handle_unauthorized():
	return jsonify(
		data={},
		message='You are not authorized to do that',
		status=401), 401

# 404 handler
@app.errorhandler(404)
def handle_404(err):
	return jsonify(
		data={},
		message='404: Resource not found',
		status=404), 404

@app.errorhandler(405)
def handle_405(err):
	return jsonify(
		data={},
		message='405: Method not allowed',
		status=405), 405

@app.route("/")
def test():
	return "server is running"

# allowed origins for CORS
origins = [
	'http://localhost:3000',
	'https://gamehoard.herokuapp.com',
	'http://gamehoard.herokuapp.com'
]

CORS(accounts, origins=origins, supports_credentials=True)
CORS(games, origins=origins, supports_credentials=True)
CORS(genres, origins=origins, supports_credentials=True)
# define routes
app.register_blueprint(accounts, url_prefix = "/api/v1/accounts")
app.register_blueprint(games, url_prefix = "/api/v1/games")
app.register_blueprint(genres, url_prefix = "/api/v1/genres")

@app.before_request
def before_request():
	print("you should see this before each request")
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	print("you should see this after each request")
	g.db.close()
	return response

if "ON_HEROKU" in os.environ:
	print("\non heroku!")
	models.initialize()

if __name__ == "__main__":
	models.initialize()
	app.run(debug=DEBUG, port=PORT)