import requests
from bs4 import BeautifulSoup


def get_all_seasons(url):
    response = requests.get(url)
    while response.status_code == 500:
        response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    seasons = []
    for div in soup.find_all("div", {"class": "card card-body"}):
        for link in div.select("a"):
            seasons.append(link['href'].split("/")[5])
    return seasons


def main():
    url = "https://www.proballers.com/basketball/league/3/nba/2020/teams"
    assert get_all_seasons(url) == [str(i) for i in range(2020, 1948, -1)]
    url = "https://www.proballers.com/basketball/league/177/euroleague/2020/teams"
    assert get_all_seasons(url) == [str(i) for i in range(2020, 1999, -1)]
    url = "https://www.proballers.com/basketball/league/100028/basketball-champions-league-americas/2020/teams"
    assert get_all_seasons(url) == ["2019"]
    print('All tests passed!!')


if __name__ == '__main__':
    main()
