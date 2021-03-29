# teams

# ----- Tests -----


def test_get_teams():
    """ Test functions:

    * get_teams_per_season()

    * get_team_details()
    """
    assert get_teams_per_season(3, "nba", 2020) == ['100', '101', '116', '825', '103', '104', '105', '106', '107',
                                                    '108',
                                                    '109', '110', '111', '112', '127', '113', '114', '115', '102',
                                                    '117',
                                                    '1827', '118', '119', '120', '121', '122', '123', '125', '126',
                                                    '128']
    assert get_team_details('100') == ['Atlanta Hawks', 'United States']
    assert get_team_details('101') == ['Boston Celtics', 'United States']
    print('All tests passed!!')