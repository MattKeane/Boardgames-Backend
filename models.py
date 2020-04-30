from peewee import *
from flask_login import UserMixin
DATABASE = SqliteDatabase("games.sqlite")

# define models

class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField()
	role = CharField() 
	bio = CharField()

	class Meta:
		database = DATABASE

class Game(Model):
	title = CharField()
	max_players = IntegerField()
	min_players = IntegerField()
	publisher = ForeignKeyField(User, backref="games")

	class Meta:
		database = DATABASE

class Genre(Model):
	name = CharField()
	description = CharField()

	class Meta:
		database = DATABASE

class GameGenreRelationship(Model):
	game = ForeignKeyField(Game, backref="game_genre_relationships")
	genre = ForeignKeyField(Genre, backref="game_genre_relationships")

	class Meta:
		database = DATABASE

class Favorite(Model):
	user = ForeignKeyField(User, backref="favorites")
	game = ForeignKeyField(User, backref="favorites")

	class Meta:
		database = DATABASE

# initialize database

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Game, Genre, GameGenreRelationship, Favorite], safe=True)
	print("Connected to DB and tables created")
	DATABASE.close()
