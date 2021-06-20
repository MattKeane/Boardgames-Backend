# Boardgames-Backend

## DataBase Structure

![DataBase Structure](https://i.imgur.com/CRulHWX.png)

## Route Structure

![Route Structure](https://i.imgur.com/Bm8Bcne.png)

## Tables

### Account

| Row      | Type        |
| -------- | ----------- |
| username | CharField() |
| email    | CharField() |
| bio      | CharField() |

### Game

| Row         | Type              |
| ----------- | ----------------- |
| title       | CharField()       |
| max_players | IntegerField()    |
| min_players | IntegerField()    |
| publisher   | ForeignKeyField() |

### Genre

| Row         | Type        |
| ----------- | ----------- |
| Name        | CharField() |
| Description | CharField() |

### Game/Genre Relationship

| Row   | Type              |
| ----- | ----------------- |
| Game  | ForeignKeyField() |
| Genre | ForeignKeyField() |

### Favorite

| Row  | Type              |
| ---- | ----------------- |
| User | ForeignKeyField() |
| Game | ForeignKeyField() |


## Routes

| Route                  | Method | Result              |
| ---------------------- | ------ | ------------------- |
| /accounts/register     | POST   | Creates an account  |
| /accounts/loign        | POST   | Logs in an account  |
| /accounts/logout       | GET    | Logs out an account |
| /genres/add            | POST   | Adds a game genre   |
| /games/                | GET    | Gets all game data  |
| /games/add             | POST   | Creates a game      |
| /games/update/\<id\>   | PUT    | Updates a game      |
| /games/delete/\<id>\>  | DELETE | Deletes a game      |
| /games/favorite/\<id\> | POST   | Favorites a game    |
| /games/favorite/\<id\> | Delete | Unfavorites a game  |

Stretch goal: add routes to allow users to search by genre.