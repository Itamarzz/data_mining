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
        print("Error 500. Trying Again...")
        response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    teams = []
    for link in soup.find_all('a', class_="home-league__team-list__content__entry-team__presentation"):
        teams.append(link['href'].split("/")[3])

    return teams


def get_team_information(url):
    response = requests.get(url)

    while response.status_code == 500:
        print("Error 500. Trying Again...")
        response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    team_description = soup.find('div', class_="home-team__content__card-identity__description")
    team_name = soup.find(class_="generic-section-subtitle").get_text()
    team_country = team_description.find('p').get_text().split("\n")[2]

    return [team_name, team_country]


def get_all_teams_information_from_league(league_id):

    url = TEAMS_PATH.format(league_id, LEAGUES[league_id], date.today().year - 1)
    all_seasons_from_leagues = get_all_seasons(url)

    count = 0
    teams = []
    for season in all_seasons_from_leagues:
        count += 1
        print(f"{count}/{len(all_seasons_from_leagues)} Seasons")
        url = TEAMS_PATH.format(league_id, LEAGUES[league_id], season)
        teams += get_teams_from_seasons(url)
    teams = list(set(teams))

    count = 0
    all_teams_with_info = {}
    for team in teams:
        count += 1
        print(f"{count}/{len(teams)} Teams")
        url = TEAM_PATH.format(team)
        all_teams_with_info[team] = get_team_information(url) + [league_id]

    df_teams = pd.DataFrame.from_dict(all_teams_with_info, orient='index').reset_index()
    df_teams.columns = ["Id", "Name", "Country", "League"]

    return df_teams


def main():
    df_teams = get_all_teams_information_from_league(3)
    print(df_teams.head())


if __name__ == '__main__':
    main()
