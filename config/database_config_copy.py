#Connection:
USERNAME = 'example_user'
PASSWORD = 'example_password'
HOST = 'localhost'
DATABASE_NAME = 'proballers'

#Tables
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
                  team_game_id varchar(20) PRIMARY KEY,\
                  game_no int,\
                  team_no int,\
                  score int,\
                  win BOOL,\
                  home bool\
                )"

PLAYER_STATS_TABLE = "CREATE TABLE player_stats (\
                      idx int PRIMARY KEY AUTO_INCREMENT,\
                      team_game_id varchar(20),\
                      player_no int,\
                      minuets int,\
                      2m int,\
                      2a int,\
                      3m int,\
                      3a int,\
                      1m int,\
                      1a int,\
                      o_r int,\
                      dr int,\
                      ast int,\
                      stl int,\
                      blk int,\
                      fo int,\
                      pts int,\
                      eff int\
                      )"


#Tables references
GAMES_LEAGUE_REF = "ALTER TABLE games ADD FOREIGN KEY (league) REFERENCES leagues (league_no)"
TEAM_GAMES_GAMES_REF = "ALTER TABLE team_games ADD FOREIGN KEY (game_no) REFERENCES games (game_no)"
TEAM_GAMES_TEAMS_REF = "ALTER TABLE team_games ADD FOREIGN KEY (team_no) REFERENCES teams (team_no)"
PLAYER_STATS_TEAM_GAMES_REF = "ALTER TABLE player_stats ADD FOREIGN KEY (team_game_id) REFERENCES team_games (team_game_id)"
PLAYER_STATS_PLAYERS_REF = "ALTER TABLE player_stats ADD FOREIGN KEY (player_no) REFERENCES `players` (player_no)"

#Database
CREATE_DATABASE = f"CREATE DATABASE {DATABASE_NAME}"
CREATE_REF = [GAMES_LEAGUE_REF, TEAM_GAMES_GAMES_REF, TEAM_GAMES_TEAMS_REF, PLAYER_STATS_TEAM_GAMES_REF, PLAYER_STATS_PLAYERS_REF]
CREATE_TABLES = [LEAGUE_TABLE, PLAYER_TABLE, TEAMS_TABLE, LEAGUE_SEASONS, GAMES_TABLE, TEAM_GAMES_TABLE, PLAYER_STATS_TABLE]
TABLE_KEYS = {'leagues': 'league_no', 'players': 'player_no', 'teams': 'team_no', 'league_seasons': 'idx',
              'games': 'game_no', 'team_games': 'team_game_id', 'player_stats': 'idx'}

#Tables
LEAGUES_TABLE_NAME = 'leagues'
PLAYERS_TABLE_NAME = 'players'
TEAMS_TABLE_NAME = 'teams'
LEAGUE_SEASONS_TABLE_NAME = 'league_seasons'
GAMES_TABLE_NAME = 'games'
TEAM_GAMES_TABLE_NAME = 'team_games'
PLAYER_STATS_TABLE_NAME = 'player_stats'