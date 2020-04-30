from peewee import *
from flask_login import UserMixin
DATABASE = SqliteDatabase("games.sqlite")

# define models

class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField()

	class Meta:
		database = DATABASE

class Game(Model):
	title = CharField()
	max_players = IntegerField()
	min_players = IntegerField()
	publisher = CharField()
	added_by = ForeignKeyField(User, backref="games")

	class Meta:
		database = DATABASE

class Genre(Model):
	name = CharField()
	game = ForeignKeyField(Game, backref="genre")

	class Meta:
		database = DATABASE

# initialize database

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Game, Genre], safe=True)
	print("Connected to DB and tables created")
	DATABASE.close()
