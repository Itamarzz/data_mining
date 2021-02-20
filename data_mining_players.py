import requests
import pandas as pd
import re

from bs4 import BeautifulSoup


def get_players():
    url = 'https://www.proballers.com/basketball/league/3/nba/2020/players'

    response = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'})
    return BeautifulSoup(response.text, 'lxml')


def get_profile(link):
    url = link
    response = requests.get(url,headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'})
    return BeautifulSoup(response.text, 'lxml')


web_players = get_players()

players = []
links = []
for a in web_players.find_all('a', class_='list-player-entry', href=True):
    players.append(a.get_text().strip())
    links.append(a['href'])

df_players = pd.DataFrame({"name": players, "link": links})
df_players.to_csv("Test.csv")

for index, row in df_players.iterrows():
    link = "https://www.proballers.com"+row['link']
    text = get_profile(link)
    break
