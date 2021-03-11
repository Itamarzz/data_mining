import config.scrapr_config as CFG
import useful_functions as uf


def get_leagues():
    soup = uf.get_source(CFG.URL_ALL_LEAGUES)
    leagues_dict = {}
    for league in soup.find_all('a', {"title": CFG.SEARCH_LINK_BY_TITLE}):
        url = league.get('href').split("/")
        leagues_dict[url[CFG.ID_LEAGUE_INDEX]] = url[CFG.NAME_LEAGUE_INDEX]

    leagues_dict = {k: v for k, v in leagues_dict.items()}
    return leagues_dict
