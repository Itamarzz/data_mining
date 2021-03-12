import config.scrapr_config as cfg
import config.database_config as dbcfg
from useful_functions import get_source, insert_rows, progress_bar, remove_existing_keys


def get_teams_per_season(league_id, league_name, season):
    """ This function returns all the teams that participated in the league league_id in the season season.
    """
    url = cfg.TEAMS_PATH.format(league_id, league_name, season)
    soup = get_source(url)

    if soup is None:
        raise TypeError("The website is not responing in this moment.")  # TODO: corregir texto

    teams = []
    for link in soup.find_all('a', class_=cfg.SEARCH_TEAM_BY_CLASS):
        teams.append(int(link['href'].split("/")[cfg.ID_TEAM_INDEX]))

    return teams


def get_team_details(team_id):
    """Returns a list with details (name, country)
        for a given team.
    """
    url = cfg.TEAM_PATH.format(team_id)
    soup = get_source(url)

    if not soup:
        return None

    team_description = soup.find('div', class_=cfg.SEARCH_TEAM_INFO_BY_CLASS)
    team_name = soup.find(class_=cfg.SEARCH_TEAM_NAME_BY_CLASS).get_text()
    team_country = team_description.find('p').get_text().split("\n")[cfg.COUNTRY_TEAM_INDEX]

    return {"name": team_name, "country": team_country}


def save_teams(league_id, league_name, season, connection):
    if not cfg.SILENT_MODE:
        print("Save teams...")

    teams_ids = get_teams_per_season(league_id, league_name, season)
    teams_ids = remove_existing_keys(dbcfg.TEAMS_TABLE_NAME, teams_ids)

    if not cfg.SILENT_MODE:
        print("Get teams list passed!")

    if len(teams_ids) > 0:
        teams_dict = {}
        len_teams = len(teams_ids)
        for index, team_id in enumerate(teams_ids):
            result = get_team_details(team_id)
            if not result:
                continue

            teams_dict[team_id] = result
            teams_dict[team_id]["team_no"] = team_id

            if not cfg.SILENT_MODE:
                progress_bar(index+1, len_teams, "Get teams details")

        if not cfg.SILENT_MODE:
            print("\nGet teams details list passed!")

        insert_rows(teams_dict, dbcfg.TEAMS_TABLE_NAME, connection)

        if not cfg.SILENT_MODE:
            print("Insert teams rows passed!")
    else:
        if not cfg.SILENT_MODE:
            print("No news teams")
        else:
            pass

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
