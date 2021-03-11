import requests
import pandas as pd
import config.scrapr_config as cfg
from bs4 import BeautifulSoup


def get_source(url):
    """ Returns a BeautifulSoup object with the source of given url """

    response = requests.get(url)
    if response.status_code not in [500, 200]:
        raise ValueError(f"Unknown request error: {response.status_code} \n url: {url}")

    count_retries = 0
    while response.status_code == 500:
        count_retries += 1
        print("Error 500. Trying Again...")
        response = requests.get(url)
        if count_retries == cfg.MAX_RETRIES:
            raise ValueError(f"Max errors: {response.status_code} \n url: {url}")

    soup = BeautifulSoup(response.text, 'lxml')

    return soup


def get_all_seasons(url):
    response = requests.get(url)

    if response.status_code not in [500, 200]:
        print(f"Unknown request error: {response.text}")
        return

    while response.status_code == 500:
        response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    seasons = []
    for div in soup.find_all("div", {"class": "card card-body"}):
        for link in div.select("a"):
            seasons.append(link['href'].split("/")[5])
    return seasons


def get_seasons_list(league_id, league_name):
    soup = get_source(cfg.TEAMS_PATH.format(league_id, league_name, 0))
    seasons = []
    for div in soup.find_all("div", {"class": "card card-body"}):
        for link in div.select("a"):
            seasons.append(link['href'].split("/")[5])
    return seasons


def insert_rows(data, table, connection, chunk_size=1000, data_types=None, index=False):
    try:
        df = pd.DataFrame.from_dict(data, orient='index')
    except Exception as ex:
        raise ValueError("Error creating DataFrame")

    if data_types:
        if not isinstance(data_types, dict):
            raise ValueError("data_types must by dictionary")
        if len(df.columns) != len(data_types):
            raise ValueError("data_types mission columns")

        for column, column_type in data_types.items():
            if type == "date":
                df[column] = pd.to_datetime(df[column])
            elif type in ["int", "str", "bool"]:
                df[column] = df[column].astype(column_type)
            else:
                raise ValueError("type not exist")

    df.to_sql(table, con=connection, if_exists='append', chunksize=chunk_size, index=index)
