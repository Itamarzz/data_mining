import logging

# Connection:

USERNAME = 'root'
PASSWORD = 'root'
HOST = 'localhost'
DATABASE_NAME = 'proballers'

# table fields and types"

LEAGUES = {'league_no': 'int', 'name': 'str'}
PLAYERS = {'player_no': 'int', 'name': 'str', 'date_of_birth': 'date',
           'height': 'float', 'position': 'str', 'nationality': 'str'}
TEAMS = {'team_no': 'int', 'name': 'str', 'country': 'str'}
GAMES = {'game_no': 'int', 'league': 'int', 'game_date': 'date', 'season': 'int'}
TEAM_GAMES = {'team_game_id': 'str', 'game_no': 'int', 'team_no': 'int',
              'score': 'int', 'win': 'bool', 'home': 'bool'}
PLAYER_STATS = {'team_game_id': 'str', 'player_no': 'int', 'minuets': 'int',
                '2m': 'int', '2a': 'int', '3m': 'int', '3a': 'int', '1m': 'int',
                '1a': 'int', 'o_r': 'int', 'dr': 'int', 'ast': 'int', 'stl': 'int',
                'blk': 'int', 'fo': 'int', 'pts': 'int', 'eff': 'int'}
LEAGUE_SEASONS = {'league_no': 'int', 'season': 'int'}

PLAYER_SUMMARY_SEASON = {'player_no': 'int', 'season': 'int', 'ppg': 'float', 'rpg': 'float', 'apg': 'float',
                         'mpg': 'float', 'topg': 'float', 'spg': 'float', 'bpg': 'float', 'tpp': 'float',
                         'ftp': 'float', 'fgp': 'float', 'assists': 'int', 'blocks': 'int', 'steals': 'int',
                         'turnovers': 'int'}

TABLES = {'leagues': LEAGUES, 'players': PLAYERS, 'teams': TEAMS,
          'games': GAMES, 'team_games': TEAM_GAMES, 'player_stats': PLAYER_STATS,
          'player_summary_season': PLAYER_SUMMARY_SEASON}

# SQL statements to create tables

CREATE_LEAGUE_TABLE = "CREATE TABLE IF NOT EXISTS leagues (\
              league_no int PRIMARY KEY,\
              name varchar(30),\
              url varchar(512)\
            )"

CREATE_PLAYER_TABLE = "CREATE TABLE IF NOT EXISTS  players ( \
              player_no int PRIMARY KEY, \
              name varchar(30),\
              date_of_birth date,\
              height float,\
              position varchar(20),\
              nationality varchar(60)\
            )"

CREATE_TEAMS_TABLE = "CREATE TABLE IF NOT EXISTS  teams (\
                team_no int PRIMARY KEY,\
                name varchar(30),\
                country varchar(60)\
                )"

CREATE_LEAGUE_SEASONS = "CREATE TABLE IF NOT EXISTS  league_seasons (\
              idx int PRIMARY KEY AUTO_INCREMENT,\
              league_no int,\
              season int,\
              status varchar(20)\
            )"

CREATE_GAMES_TABLE = "CREATE TABLE IF NOT EXISTS  games (\
              game_no int PRIMARY KEY,\
              league int,\
              game_date date,\
              season int\
            )"

CREATE_TEAM_GAMES_TABLE = "CREATE TABLE IF NOT EXISTS  team_games (\
                  team_game_id varchar(20) PRIMARY KEY,\
                  game_no int,\
                  team_no int,\
                  score int,\
                  win BOOL,\
                  home bool\
                )"

CREATE_PLAYER_STATS_TABLE = "CREATE TABLE IF NOT EXISTS  player_stats (\
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

CREATE_PLAYER_SUMMARY_SEASON_TABLE = "CREATE TABLE IF NOT EXISTS player_summary_season (\
                        idx int PRIMARY KEY AUTO_INCREMENT,\
                        player_no int,\
                        season int,\
                        ppg float,\
                        rpg float,\
                        apg float,\
                        mpg float,\
                        topg float,\
                        spg float,\
                        bpg float,\
                        tpp float,\
                        ftp float,\
                        fgp float,\
                        assists int,\
                        blocks int,\
                        steals int,\
                        turnovers int\
                      )"

# Tables references
GAMES_LEAGUE_REF = "ALTER TABLE games ADD FOREIGN KEY (league) REFERENCES leagues (league_no)"
TEAM_GAMES_GAMES_REF = "ALTER TABLE team_games ADD FOREIGN KEY (game_no) REFERENCES games (game_no)"
TEAM_GAMES_TEAMS_REF = "ALTER TABLE team_games ADD FOREIGN KEY (team_no) REFERENCES teams (team_no)"
PLAYER_STATS_TEAM_GAMES_REF = """ALTER TABLE player_stats ADD FOREIGN KEY (team_game_id)
                                REFERENCES team_games (team_game_id)"""
PLAYER_STATS_PLAYERS_REF = "ALTER TABLE player_stats ADD FOREIGN KEY (player_no) REFERENCES `players` (player_no)"
PLAYER_SUMMARY_SEASON_REF = """ALTER TABLE player_summary_season ADD FOREIGN KEY (player_no) REFERENCES `players`
                        (player_no)"""

# Database
CREATE_DATABASE = f"CREATE DATABASE IF NOT EXISTS  {DATABASE_NAME}"
CREATE_REF = [GAMES_LEAGUE_REF, TEAM_GAMES_GAMES_REF, TEAM_GAMES_TEAMS_REF, PLAYER_STATS_TEAM_GAMES_REF,
              PLAYER_STATS_PLAYERS_REF, PLAYER_SUMMARY_SEASON_REF]
CREATE_TABLES = [CREATE_LEAGUE_TABLE, CREATE_PLAYER_TABLE, CREATE_TEAMS_TABLE, CREATE_LEAGUE_SEASONS,
                 CREATE_GAMES_TABLE, CREATE_TEAM_GAMES_TABLE, CREATE_PLAYER_STATS_TABLE,
                 CREATE_PLAYER_SUMMARY_SEASON_TABLE]

TABLE_KEYS = {'leagues': 'league_no', 'players': 'player_no', 'teams': 'team_no', 'league_seasons': 'idx',
              'games': 'game_no', 'team_games': 'team_game_id', 'player_stats': 'idx', 'player_summary_season': 'idx'}

# Tables
LEAGUES_TABLE_NAME = 'leagues'
PLAYERS_TABLE_NAME = 'players'
TEAMS_TABLE_NAME = 'teams'
LEAGUE_SEASONS_TABLE_NAME = 'league_seasons'
GAMES_TABLE_NAME = 'games'
TEAM_GAMES_TABLE_NAME = 'team_games'
PLAYER_STATS_TABLE_NAME = 'player_stats'
PLAYER_SUMMARY_SEASON_TABLE_NAME = 'player_summary_season'

# logger

# logger

LOG_FILE = 'db.log'
MAIN_FORMATTER = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
