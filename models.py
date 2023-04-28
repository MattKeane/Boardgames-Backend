import os
from peewee import *
from flask_login import UserMixin
from playhouse.db_url import connect
from flask_bcrypt import generate_password_hash

if "ON_HEROKU" in os.environ:
	DATABASE = connect(os.environ.get("DATABASE_URL"))
else:
	DATABASE = SqliteDatabase("games.sqlite",
		pragmas = {"foreign_keys": 1})

# custom password field

class PasswordField(CharField):
	def db_value(self, value):
		hashed_password = generate_password_hash(value)
		return super().db_value(hashed_password)

# define models

class Account(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = PasswordField()
	role = CharField() 
	bio = CharField(default="")

	class Meta:
		database = DATABASE

class Game(Model):
	title = CharField()
	max_players = IntegerField()
	min_players = IntegerField()
	publisher = ForeignKeyField(Account, backref="games")

	class Meta:
		database = DATABASE

class Genre(Model):
	name = CharField()
	description = CharField()

	class Meta:
		database = DATABASE

class GameGenreRelationship(Model):
	game = ForeignKeyField(Game, backref="game_genre_relationships", on_delete="CASCADE")
	genre = ForeignKeyField(Genre, backref="game_genre_relationships", on_delete="CASCADE")

	class Meta:
		database = DATABASE

class Favorite(Model):
	user = ForeignKeyField(Account, backref="favorites", on_delete="CASCADE")
	game = ForeignKeyField(Game, backref="favorites", on_delete="CASCADE")

	class Meta:
		database = DATABASE

# initialize database

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Account, Game, Genre, GameGenreRelationship, Favorite], safe=True)
	print("Connected to DB and tables created")
	DATABASE.close()
