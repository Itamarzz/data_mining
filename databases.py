from dateutil.parser import parse


def get_height_meters(height):
    """ Returns height in meters as a float.
        input: string of height in meters and feet
        output: float """

    height_m = height.split(' / ')[0]
    height_m = height_m.replace('m', '.')
    height_m = float(height_m)

    return height_m


def get_player_id_dict(id_card):
    """ receives player_id_card as a dictionary with raw data
        returns : dictionary after setting suitable data type for each value """

    id_dict['id'] = int(id_card['id'])
    id_dict['name'] = id_card['name']
    id_dict['date_of_birth'] = parse(id_card['Date of birth']).date()
    id_dict['height'] = get_height_meters(id_card['Height'])
    id_dict['position'] = id_card['Position']
    id_dict['position'] = id_card['Position']
    id_dict['nationality'] = id_card['Nationality']
    id_dict['draft'] = id_card['Draft']

    # columns = ['Height', 'University', 'name', 'Date of birth', 'Nationality', 'Draft', 'Social', 'Position', 'p_id']

    return id_dict
