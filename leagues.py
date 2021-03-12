import config.scrapr_config as cfg
import config.database_config as dbcfg
import useful_functions as uf
from useful_functions import get_source, insert_rows, progress_bar, remove_existing_keys

def get_leagues():
    """ Returns a list of all available leagues for scrapping from the Proballers web site
    """
    
    soup = uf.get_source(cfg.URL_ALL_LEAGUES)
    leagues_dict = {}
    for league in soup.find_all('a', {"title": cfg.SEARCH_LINK_BY_TITLE}):
        url = league.get('href').split("/")
        leagues_dict[url[cfg.ID_LEAGUE_INDEX]] = url[cfg.NAME_LEAGUE_INDEX]

    leagues_dict = {k: v for k, v in leagues_dict.items()}
    return leagues_dict


def save_league(league_no, league_name, connection, chunk_size):
    """ inserts to database scrapped data to the league table
    """
    
    if not cfg.SILENT_MODE:
        print("Save league...")

    if len(remove_existing_keys(dbcfg.LEAGUES_TABLE_NAME, [int(league_no)])) != 0:
        league_info = {league_no: {"league_no": league_no, "name": league_name}}
        insert_rows(league_info, dbcfg.LEAGUES_TABLE_NAME, connection, chunk_size)
        if not cfg.SILENT_MODE:
            print("Insert league row passed!")
    else:
        if not cfg.SILENT_MODE:
            print("Not news leagues")

