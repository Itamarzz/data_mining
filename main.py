import sys
import config.scrapr_config as cfg
import argparse
import scraper
import db


def parse_args():
    """ returns user input from terminal
    """

    parser = argparse.ArgumentParser(description=str(cfg.DESCRIPTION))
    parser.add_argument('-l', '--league', type=str, metavar='',
                        help='use -a to print available list of leagues to scrape')
    parser.add_argument('-s', '--season', type=int, metavar='', help='season to scrape, input first year of season')
    parser.add_argument('-c', '--chunk_size', type=int, metavar='', help='set chunk size for insertion to the database')
    parser.add_argument('-gl', '--games_limit', type=int, metavar='', help='set limit to max number of games to scrap')
    parser.add_argument('-a', '--availability', action='store_true', help='print all available leagues to scrape')

    return parser.parse_args()


def get_league_no(league, available_leagues):
    """ checks if user input for league to scrape is valid and available and returns league number
    """

    if league not in available_leagues.values():
        raise ValueError(f'League name not exist')

    for league_no, name in available_leagues.items():
        if name == league:
            return league_no


def validate_season(league_id, league_name, season):
    """ checks if user input for season to scrape is valid and available
    """

    seasons_list = scraper.get_seasons_list(league_id, league_name)
    if str(season) not in seasons_list:
        raise ValueError(f'Season not exist')


def get_chunk_size(args):
    """ returns valid chunk size
    """

    if args.chunk_size:
        if args.chunk_size > 0:
            chunk_size = args.chunk_size
        else:
            print('invalid chunk size. chunk size must be positive integer')
            sys.exit(1)
    else:
        chunk_size = cfg.CHUNK

    return chunk_size


def get_games_limit(args):
    """ returns valid games limit value
    """

    if args.games_limit:
        if args.games_limit >= 0:
            games_limit = args.games_limit
        else:
            print('invalid games_limit value. in order to limit max games\
                to be scrapped please make sure to provide non negative value')
            sys.exit(1)
    else:
        games_limit = cfg.GAME_LIMIT

    return games_limit


def validate_input(args, available_leagues):
    """ validate input of league and season
    """

    if (not args.league) or (not args.season):
        print(cfg.HELP_STRING)
        sys.exit(1)
    else:
        league_name = args.league
        season = args.season
        league_no = get_league_no(league_name, available_leagues)
        validate_season(league_no, league_name, season)

    chunk_size = get_chunk_size(args)
    games_limit = get_games_limit(args)

    return league_no, league_name, season, chunk_size, games_limit


def print_leagues(leagues):
    """ prints all available leagues
    """
    print("\n#---------- available leagues: ----------#\n")
    for k, v in leagues.items():
        print(f"{k}, {v}")


def main():
    """ takes arguments from terminal using parse_args func, validate input through validation functions 
    and call scraping function to scrape and insert data to the database from the relevant modules
    """

    try:
        args = parse_args()
        available_leagues = scraper.get_leagues()
        if args.availability:
            print_leagues(available_leagues)
        else:
            league_no, league_name, season, chunk_size, games_limit = validate_input(args, available_leagues)

            db.use_database()
            data = scraper.scraper(league_no, league_name, season, games_limit)
            db.insert_dict_to_df(data, chunk_size)


    except ValueError as ex:
        print(f'ERROR: Invalid input: {ex}\nFor proper usage:\n{cfg.HELP_STRING}', )
    else:
        print(f'\nSUCCESS!!\n ', ' ')


if __name__ == '__main__':
    main()
