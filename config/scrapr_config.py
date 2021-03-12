PATH_ROOT = "https://www.proballers.com"
MAX_RETRIES = 5
SILENT_MODE = False

#Leagues Config
URL_ALL_LEAGUES = "https://www.proballers.com/page/7-leagues-we-cover"
ID_LEAGUE_INDEX = 3
NAME_LEAGUE_INDEX = 4
SEARCH_LINK_BY_TITLE = "Player list"

#Teams Config
TEAMS_PATH = PATH_ROOT+"/basketball/league/{}/{}/{}/teams"
TEAM_PATH = PATH_ROOT+"/basketball/team/{}"
SEARCH_TEAM_BY_CLASS = "home-league__team-list__content__entry-team__presentation"
ID_TEAM_INDEX = 3
SEARCH_TEAM_INFO_BY_CLASS = "home-team__content__card-identity__description"
SEARCH_TEAM_NAME_BY_CLASS = "generic-section-subtitle"
COUNTRY_TEAM_INDEX = 2

#Games Config
GAMES_PATH = PATH_ROOT + "/basketball/league/{}/{}/{}/schedule"
GAME_PATH = PATH_ROOT + "/basketball/game/{}"
SEARCH_PAGINATION_BY_CLASS = "pagination-link"
SEARCH_GAMES_IDS_BY_CLASS = "home-league__schedule__content__tables__content"
SEARCH_GAME_TEAMS_BY_CLASS = "home-game__content__result__final-score__team__picture"
SEARCH_GAME_RESULT_BY_CLASS = "home-game__content__result__final-score__score"
GAME_NAME = 'game'
ID_GAME_INDEX = 3

#Players Config
PLAYER_PATH = PATH_ROOT + '/basketball/player/{}'



# main - user interface

NUM_ARGS_NO_ARGS = 1

DESCRIPTION = "scrape the Proballers and save it to the proballers database"

HELP_STRING= '\n#---------- Hello and Welcome to the Proballers Scraper !!! ---------#\n\n' \
          'in order to start scraping two arguments are required:\n' \
          '1. -l <league name> -->      use -a or --availability to print list of available leagues\n' \
          '2. -s <year> -->      where year is the first year of the required season.\n' \
             '                   so for season 2015-2016 --> year = 2015\n' \
          'please make sure to provide both\n\n' \
          'for example: if you want to scrap the NBA league in season 2018-2019:\n' \
          '             the input shoud be: "-l nba -s 2018\n\n ' \
          'for more info use the --help'

# insertion to db:

CHUNK = 1000
GAME_LIMIT = None