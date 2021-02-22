import requests
import pandas as pd
from bs4 import BeautifulSoup
from useful_functions import get_all_seasons
from datetime import date

ROOT = "https://www.proballers.com"
LEAGUES = {3: 'nba'}
TEAMS_PATH = ROOT+"/basketball/league/{}/{}/{}/teams"
TEAM_PATH = ROOT+"/basketball/team/{}"


def get_teams_from_seasons(league_id, season):
    """ This function returns all the teams that participated in the league league_id in the season season.
    """
    url = TEAMS_PATH.format(league_id, LEAGUES[league_id], season)
    response = requests.get(url)

    if response.status_code not in [500, 200]:
        print(f"Unknown request error: {response.text}")
        return

    while response.status_code == 500:
        print("Error 500. Trying Again...")
        response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    teams = []
    for link in soup.find_all('a', class_="home-league__team-list__content__entry-team__presentation"):
        teams.append(link['href'].split("/")[3])

    return teams


def get_team_information(team_id):
    """This function returns the name and the country to which the team team_id belongs
    """
    url = TEAM_PATH.format(team_id)
    response = requests.get(url)

    if response.status_code not in [500, 200]:
        print(f"Unknown request error: {response.text}")
        return

    while response.status_code == 500:
        print("Error 500. Trying Again...")
        response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    team_description = soup.find('div', class_="home-team__content__card-identity__description")
    team_name = soup.find(class_="generic-section-subtitle").get_text()
    team_country = team_description.find('p').get_text().split("\n")[2]

    return [team_name, team_country]


def get_all_teams_information_from_league(league_id):
    """ This function returns a DataFrame with information on all the teams that have participated in the
    league league_id in any season.
    """
    url = TEAMS_PATH.format(league_id, LEAGUES[league_id], date.today().year - 1)
    all_seasons_from_leagues = get_all_seasons(url)

    teams = []
    count, len_all_seasons_from_leagues = 0, len(all_seasons_from_leagues)
    print("Get all teams per seasons...")
    for season in all_seasons_from_leagues:
        count += 1
        print(f"{count}/{len_all_seasons_from_leagues} Season {season}...")
        teams += get_teams_from_seasons(league_id, season)
    teams = list(set(teams))

    all_teams_with_info = {}
    count, len_teams = 0, len(teams)
    print("Get team information...")
    for team_id in teams:
        count += 1
        print(f"{count}/{len_teams} Teams {team_id}...")
        all_teams_with_info[team_id] = get_team_information(team_id) + [league_id]

    df_teams = pd.DataFrame.from_dict(all_teams_with_info, orient='index').reset_index()
    df_teams.columns = ["Id", "Name", "Country", "League"]

    return df_teams


def main():
    """ Test functions:

    * get_teams_from_seasons()

    * get_team_information()

    * get_all_teams_information_from_league()
    """
    assert get_teams_from_seasons(3, 2020) == ['100', '101', '116', '825', '103', '104', '105', '106', '107', '108',
                                               '109', '110', '111', '112', '127', '113', '114', '115', '102', '117',
                                               '1827', '118', '119', '120', '121', '122', '123', '125', '126', '128']
    assert get_team_information('100') == ['Atlanta Hawks', 'United States']
    assert get_team_information('101') == ['Boston Celtics', 'United States']
    df_teams = get_all_teams_information_from_league(3)
    print(df_teams.head())
    print('All tests passed!!')


if __name__ == '__main__':
    main()
