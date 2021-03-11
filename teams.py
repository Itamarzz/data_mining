import config.scrapr_config as cfg
import config.database_config as dbcfg
from useful_functions import get_source, insert_rows


def get_teams_per_season(league_id, league_name, season):
    """ This function returns all the teams that participated in the league league_id in the season season.
    """
    url = cfg.TEAMS_PATH.format(league_id, league_name, season)
    soup = get_source(url)

    teams = []
    for link in soup.find_all('a', class_=cfg.SEARCH_TEAM_BY_CLASS):
        teams.append(link['href'].split("/")[cfg.ID_TEAM_INDEX])

    return teams


def get_team_details(team_id):
    """Returns a list with details (name, country)
        for a given team.
    """
    url = cfg.TEAM_PATH.format(team_id)
    soup = get_source(url)

    team_description = soup.find('div', class_=cfg.SEARCH_TEAM_INFO_BY_CLASS)
    team_name = soup.find(class_=cfg.SEARCH_TEAM_NAME_BY_CLASS).get_text()
    team_country = team_description.find('p').get_text().split("\n")[cfg.COUNTRY_TEAM_INDEX]

    return {"name": team_name, "country": team_country}


def save_teams(league_id, league_name, season, connection):
    teams_dict = {}
    teams_list = get_teams_per_season(league_id, league_name, season)

    for team_id in teams_list:
        teams_dict[team_id] = get_team_details(team_id)
        teams_dict[team_id]["team_no"] = team_id

    insert_rows(teams_dict, dbcfg.TEAMS_TABLE_NAME, connection)

# ----- Tests -----


def test_get_teams():
    """ Test functions:

    * get_teams_per_season()

    * get_team_details()
    """
    assert get_teams_per_season(3, "nba", 2020) == ['100', '101', '116', '825', '103', '104', '105', '106', '107', '108',
                                             '109', '110', '111', '112', '127', '113', '114', '115', '102', '117',
                                             '1827', '118', '119', '120', '121', '122', '123', '125', '126', '128']
    assert get_team_details('100') == ['Atlanta Hawks', 'United States']
    assert get_team_details('101') == ['Boston Celtics', 'United States']
    print('All tests passed!!')
#test_get_teams()
