import requests
import pandas as pd
from bs4 import BeautifulSoup
from useful_functions import get_all_seasons
from datetime import date

ROOT = "https://www.proballers.com"
LEAGUES = {3: 'nba'}
TEAMS_PATH = ROOT+"/basketball/league/{}/{}/{}/teams"
TEAM_PATH = ROOT+"/basketball/team/{}"


def get_teams_from_seasons(url):
    response = requests.get(url)
    while response.status_code == 500:
        response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    teams = []
    for link in soup.find_all('a', class_="home-league__team-list__content__entry-team__presentation"):
        teams.append(link['href'].split("/")[3])

    return teams


def get_team_information(url):
    response = requests.get(url)

    while response.status_code == 500:
        response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    team_description = soup.find('div', class_="home-team__content__card-identity__description")
    team_name = soup.find(class_="generic-section-subtitle").get_text()
    team_country = team_description.find('p').get_text().split("\n")[2]

    return [team_name, team_country]


def get_all_teams_information_from_leagues(leagues_dict):
    all_seasons_from_leagues = {}
    for league_id, name in leagues_dict.items():
        url = TEAMS_PATH.format(league_id, name, date.today().year - 1)
        all_seasons_from_leagues[league_id] = get_all_seasons(url)

    all_team_from_leagues = {}
    for league, seasons in all_seasons_from_leagues.items():
        teams_aux = []
        for season in seasons:
            url = TEAMS_PATH.format(league, leagues_dict[league], season)
            teams_aux += get_teams_from_seasons(url)
        all_team_from_leagues[league] = list(set(teams_aux))

    all_teams_with_info = {}
    for league, teams in all_team_from_leagues.items():
        for team in teams:
            url = TEAM_PATH.format(team)
            all_teams_with_info[team] = get_team_information(url) + [league]

    df_teams = pd.DataFrame.from_dict(all_teams_with_info, orient='index').reset_index()
    df_teams.columns = ["Id", "Name", "Country", "League"]
    return df_teams


def main():
    df_teams = get_all_teams_information_from_leagues(LEAGUES)
    print(df_teams.head())


if __name__ == '__main__':
    main()
