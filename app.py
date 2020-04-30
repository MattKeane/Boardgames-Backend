# modules
from flask import Flask 

# models
import models

# blueprints
from resources.users import users

DEBUG=True
PORT=8000

app = Flask(__name__)

@app.route("/")
def test():
	return "server is running"

# define routes
app.register_blueprint(users, url_prefix = "/api/v1/users")

if __name__ == "__main__":
	models.initialize()
	app.run(debug=DEBUG, port=PORT)