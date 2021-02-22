import pandas as pd
from useful_functions import get_all_seasons, get_source
from datetime import date

ROOT = "https://www.proballers.com"
LEAGUES = {3: 'nba'}
TEAMS_PATH = ROOT+"/basketball/league/{}/{}/{}/teams"
TEAM_PATH = ROOT+"/basketball/team/{}"


def get_teams_per_season(league_id, season):
    """ This function returns all the teams that participated in the league league_id in the season season.
    """
    url = TEAMS_PATH.format(league_id, LEAGUES[league_id], season)
    soup = get_source(url)

    teams = []
    for link in soup.find_all('a', class_="home-league__team-list__content__entry-team__presentation"):
        teams.append(link['href'].split("/")[3])

    return teams


def get_team_details(team_id):
    """Returns a list with details (name, country)
        for a given team.
    """
    url = TEAM_PATH.format(team_id)
    soup = get_source(url)

    team_description = soup.find('div', class_="home-team__content__card-identity__description")
    team_name = soup.find(class_="generic-section-subtitle").get_text()
    team_country = team_description.find('p').get_text().split("\n")[2]

    return [team_name, team_country]


def get_teams_from_league(league_id):
    """ Returns a pandas data frame with all team results of a given league
    """
    url = TEAMS_PATH.format(league_id, LEAGUES[league_id], date.today().year - 1)
    all_seasons_from_league = get_all_seasons(url)

    teams_id = []
    count, len_all_seasons_from_leagues = 0, len(all_seasons_from_league)
    print(f"Get all teams in league {league_id},{LEAGUES[league_id]} per season")
    for season in all_seasons_from_league:
        count += 1
        print(f"{count}/{len_all_seasons_from_leagues} Season {season}...")
        teams_id += get_teams_per_season(league_id, season)
    teams_id = list(set(teams_id))

    teams = {}
    count, len_teams = 0, len(teams_id)
    for team_id in teams_id:
        count += 1
        print(f"{count}/{len_teams} Team Id {team_id}...")
        teams[team_id] = get_team_details(team_id) + [league_id]

    df_teams = pd.DataFrame.from_dict(teams, orient='index').reset_index()
    df_teams.columns = ["Id", "Name", "Country", "League"]

    return df_teams

# ----- Tests -----


def test_get_teams():
    """ Test functions:

    * get_teams_per_season()

    * get_team_details()
    """
    assert get_teams_per_season(3, 2020) == ['100', '101', '116', '825', '103', '104', '105', '106', '107', '108',
                                             '109', '110', '111', '112', '127', '113', '114', '115', '102', '117',
                                             '1827', '118', '119', '120', '121', '122', '123', '125', '126', '128']
    assert get_team_details('100') == ['Atlanta Hawks', 'United States']
    assert get_team_details('101') == ['Boston Celtics', 'United States']
    print('All tests passed!!')
# test_get_teams()


def main():

    LEAGUE_ID = 3  # sample league_id

    df_teams = get_teams_from_league(LEAGUE_ID)
    print(df_teams.head())


if __name__ == '__main__':
    main()
