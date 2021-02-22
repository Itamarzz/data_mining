import requests
from bs4 import BeautifulSoup


def get_source(url):
    """ Returns a BeautifulSoup object with the source of given url """

    response = requests.get(url)
    if response.status_code not in [500, 200]:
        print(f"Unknown request error: {response.text}")
        return

    while response.status_code == 500:
        print("Error 500. Trying Again...")
        response = requests.get(url)

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


# TODO: Explicar porque sirve poner en el link 2020.

def main():
    url = "https://www.proballers.com/basketball/league/3/nba/2020/players"
    assert get_all_seasons(url) == [str(i) for i in range(2020, 1948, -1)]
    url = "https://www.proballers.com/basketball/league/177/euroleague/2020/teams"
    assert get_all_seasons(url) == [str(i) for i in range(2020, 1999, -1)]
    url = "https://www.proballers.com/basketball/league/100028/basketball-champions-league-americas/2020/teams"
    assert get_all_seasons(url) == ["2019"]
    print('All tests passed!!')


if __name__ == '__main__':
    main()
