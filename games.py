import requests
import pandas as pd
from bs4 import BeautifulSoup
from useful_functions import get_all_seasons
from datetime import date

ROOT = "https://www.proballers.com"
LEAGUES = {3: 'nba'}
SCHEDULES_PATH = ROOT+"/basketball/league/{}/{}/{}/schedule"
SCHEDULE_PATH = ROOT+"/basketball/game/{}"


def get_pagination(url):
    response = requests.get(url)
    while response.status_code == 500:
        print("Error 500. Trying Again...")
        response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    pagination = []
    for div in soup.find_all("a", {"class": "pagination-link"}):
        pagination.append(int(div.get_text()))
    return int(max(pagination))


def get_games_ids(url):
    response = requests.get(url)
    while response.status_code == 500:
        print("Error 500. Trying Again...")
        response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    games = []
    for div in soup.find_all("div", {"class": "home-league__schedule__content__tables__content"}):
        for link in div.select("a"):
            if 'game' in link['href']:
                games.append(link['href'].split("/")[3])
    return games


def get_game_information(url):
    response = requests.get(url)
    while response.status_code == 500:
        print("Error 500. Trying Again...")
        response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    teams = []
    for team in soup.find_all('a', class_="home-game__content__result__final-score__team__picture"):
        teams.append(team['href'].split("/")[3])
    local_team, visit_team = teams

    span_info = []
    for div in soup.select('div.home-game__content__result__final-score__score'):
        for span in div.select('span'):
            span_info.append(span.get_text())
    match_date, results, status = span_info
    local_score, visit_score = results.split(" - ")
    return [local_team, visit_team, match_date, status, local_score, visit_score]


def get_all_games_information_from_league(league_id):
    url = SCHEDULES_PATH.format(league_id, LEAGUES[league_id], date.today().year - 1)
    all_seasons_from_leagues = get_all_seasons(url)

    count = 0
    all_games = {}
    for season in all_seasons_from_leagues:
        count += 1
        print(f"{count}/{len(all_seasons_from_leagues)} Seasons")
        url = SCHEDULES_PATH.format(league_id, LEAGUES[league_id], season)
        games_aux = []
        for i in range(1, get_pagination(url)):
            url_pag = SCHEDULES_PATH.format(league_id, LEAGUES[league_id], season) + "/" + str(i)
            games_aux += get_games_ids(url_pag)
        all_games[season] = games_aux
        break

    count_season = 0
    all_games_with_info = {}
    for season, games in all_games.items():
        count_games = 0
        count_season += 1
        for game in games:
            count_games += 1
            print(f"Season {season} ({count_season}/{len(all_games.keys())}). Games ({count_games}/{len(games)})")
            url = SCHEDULE_PATH.format(game)
            all_games_with_info[game] = [league_id, season] + get_game_information(url)

    df_games = pd.DataFrame.from_dict(all_games_with_info, orient='index').reset_index()
    df_games.columns = ["Id", "League", "Year", "Local Team", "Visiting Team", "Date", "Status", "Local Score",
                        "Visiting Score"]
    return df_games


def main():
    df_teams = get_all_games_information_from_league(3)
    print(df_teams.head())


if __name__ == '__main__':
    main()
