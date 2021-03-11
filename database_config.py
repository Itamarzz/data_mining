# import database as db
import pandas as pd

### Tables :

LEAGUE_TABLE = "CREATE TABLE leagues (\
              league_no int PRIMARY KEY,\
              name varchar(30),\
              url varchar(512)\
            )"

PLAYER_TABLE = "CREATE TABLE players ( \
              player_no int PRIMARY KEY, \
              name varchar(30),\
              date_of_birth date,\
              height float,\
              position varchar(20),\
              nationality varchar(60)\
            )"

TEAMS_TABLE = "CREATE TABLE teams (\
                team_no int PRIMARY KEY,\
                name varchar(30),\
                country varchar(60)\
                )"

LEAGUE_SEASONS = "CREATE TABLE league_seasons (\
              idx int PRIMARY KEY,\
              league_no int,\
              season varchar(10),\
              status varchar(20)\
            )"

GAMES_TABLE = "CREATE TABLE games (\
              game_no int PRIMARY KEY,\
              league int,\
              game_date date,\
              Season varchar(10)\
            )"

TEAM_GAMES_TABLE = "CREATE TABLE team_games (\
                  team_game_id int PRIMARY KEY,\
                  game_no int,\
                  team_no int,\
                  score int,\
                  win BOOL\
                )"

PLAYER_STATS_TABLE = "CREATE TABLE player_stats (\
                      idx int PRIMARY KEY AUTO_INCREMENT,\
                      team_game_id int,\
                      player_no int,\
                      minuets int,\
                      2M int,\
                      2A int,\
                      3M int,\
                      3A int,\
                      1M int,\
                      1A int,\
                      O_r int,\
                      Dr int,\
                      Ast int,\
                      Stl int,\
                      Blk int,\
                      fo int,\
                      Pts int,\
                      Eff int\
                      )"


# Tables references:

GAMES_LEAGUE_REF = "ALTER TABLE games ADD FOREIGN KEY (league) REFERENCES leagues (league_no)"

TEAM_GAMES_GAMES_REF = "ALTER TABLE team_games ADD FOREIGN KEY (game_no) REFERENCES games (game_no)"

TEAM_GAMES_TEAMS_REF = "ALTER TABLE team_games ADD FOREIGN KEY (team_no) REFERENCES teams (team_no)"

PLAYER_STATS_TEAM_GAMES_REF = "ALTER TABLE player_stats ADD FOREIGN KEY (team_game_id) REFERENCES team_games (team_game_id)"

PLAYER_STATS_PLAYERS_REF = "ALTER TABLE player_stats ADD FOREIGN KEY (player_no) REFERENCES `players` (player_no)"

# REF_LEGEUE_SEASON_LEAGUES= "ALTER TABLE league_seasons ADD FOREIGN KEY (league_no) REFERENCES leagues (league_no)"


### database:

DATABASE_NAME = 'proballers'

CREATE_DATABASE = f"CREATE DATABASE {DATABASE_NAME}"


CREATE_REF = [GAMES_LEAGUE_REF, TEAM_GAMES_GAMES_REF, TEAM_GAMES_TEAMS_REF, PLAYER_STATS_TEAM_GAMES_REF, PLAYER_STATS_PLAYERS_REF]

CREATE_TABLES = [LEAGUE_TABLE, PLAYER_TABLE, TEAMS_TABLE, LEAGUE_SEASONS, GAMES_TABLE, TEAM_GAMES_TABLE, PLAYER_STATS_TABLE]

TABLE_NAMES = ['leagues', 'players', 'teams', 'league_seasons', 'games', 'team_games', 'player_stats']

### SQL connection:

USERNAME = 'root'
PASSWORD = 'root'
HOST = 'localhost'

# con = db.connect_sql()

# df = sql_query("show databases")

# print(con)
