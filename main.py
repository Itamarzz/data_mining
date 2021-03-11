import sys
import leagues as lg
import useful_functions as uf
import config.scrapr_config as cfg
import config.database_config as dbcfg
import argparse

from sqlalchemy import create_engine
from teams import save_teams
from games import save_games

HELP_STRING = """Welcome to the proballers scrapper!

usage: main.py [option] ... [LEAGUE] [SEASON] ...
Example Usage: main.py nba 2020
    
It is also possible to select the league by identifier --> main.py 442 2020

Available Options (Use options before positional arguments):
--player_stats: Include game player stats

Help Options:
leagues_list: Show league list
Example Usage: main.py --help leagues_list
"""

NUM_ARGS_NO_ARGS = 1


def get_and_validate_league(league):
    leagues_list = lg.get_leagues()

    if league.isdigit():
        if league not in leagues_list.keys():
            raise ValueError(f'League id not exist')
        else:
            return league, leagues_list[league]
    else:
        if league not in leagues_list.values():
            raise ValueError(f'League name not exist')
        else:
            for index, name in leagues_list.items():
                if name == league:
                    return index, league


def validate_season(league_id, league_name, season):
    seasons_list = uf.get_seasons_list(league_id, league_name)
    if season not in seasons_list:
        raise ValueError(f'Season not exist')


def main():
    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('leagues')
    # parser.add_argument('seasons')
    #
    # args = parser.parse_args()
    # print(args.accumulate(args.integers))

    if len(sys.argv) == NUM_ARGS_NO_ARGS:
        print(HELP_STRING)
        return
    elif sys.argv[1] == '--help':
        if 'leagues_list' in sys.argv:
            leagues_list = lg.get_leagues()
            for k, v in leagues_list.items():
                print(f"{k}, {v}")
            return
        else:
            print(HELP_STRING)
            return

    try:
        season = sys.argv[-1]
        league = sys.argv[-2]
        player_stats = "player_stats" in sys.argv

        league_id, league_name = get_and_validate_league(league)
        validate_season(league_id, league_name, season)
        if not cfg.SILENT_MODE:
            print("Validation Passed!")

        connection = create_engine(f'mysql+pymysql://{dbcfg.USERNAME}:{dbcfg.PASSWORD}@{dbcfg.HOST}/{dbcfg.DATABASE_NAME}')

        save_teams(league_id, league_name, season, connection)
        save_games(league_id, league_name, season, connection, player_stats)

    except Exception as ex:
        print(f'ERROR: Invalid input: {ex}\nFor proper usage:\n{HELP_STRING}', )
    else:
        print(f'SUCCESS: Result of replacing the letters is:\n ', ' ')


if __name__ == '__main__':
    main()
