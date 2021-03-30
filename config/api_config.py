import logging

NBA_URL_TEAMS_API = "http://data.nba.net/10s/prod/v1/{}/players.json"
NBA_URL_PLAYER_API = "http://data.nba.net/data/10s/prod/v1/{}/players/{}_profile.json"
API_NBA_JSON_KEY_1 = "league"
API_NBA_JSON_KEY_2 = "standard"

API_NBA_PLAYER_ID = "personId"
API_NBA_NAME_PLAYER = "Name"
API_CREATE_NAME_1 = "firstName"
API_CREATE_NAME_2 = "lastName"

API_NBA_PLAYERS_JSON_KEY_1 = "league"
API_NBA_PLAYERS_JSON_KEY_2 = "standard"
API_NBA_PLAYERS_JSON_KEY_3 = "stats"
API_NBA_PLAYERS_JSON_KEY_4 = "regularSeason"
API_NBA_PLAYERS_JSON_KEY_5 = "season"

API_NBA_PLAYERS_INFO_KEY = "total"
API_NBA_SEASON_YEAR = "seasonYear"

API_NBA_PLAYERS_INFO_COLUMNS = {'ppg', 'rpg', 'apg', 'mpg', 'topg', 'spg', 'bpg', 'tpp', 'ftp', 'fgp', 'assists',
                                'blocks', 'steals', 'turnovers'}

LOG_FILE = 'api.log'
MAIN_FORMATTER = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
