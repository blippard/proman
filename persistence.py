import csv

STATUSES_FILE = './data/statuses.csv'
BOARDS_FILE = './data/boards.csv'
CARDS_FILE = './data/cards.csv'
STATUSES_HEADER = ['id', 'title']
BOARDS_HEADER = ['id', 'title', 'board_statuses']
CARDS_HEADER = ['id', 'board_id', 'title', 'status_id', 'order']

_cache = {}  # We store cached data in this dict to avoid multiple file readings


def _read_csv(file_name):
    """
    Reads content of a .csv file
    :param file_name: relative path to data file
    :return: OrderedDict
    """
    with open(file_name) as boards:
        rows = csv.DictReader(boards, delimiter=',', quotechar='"')
        formatted_data = []
        for row in rows:
            formatted_data.append(dict(row))
        return formatted_data


def _get_data(data_type, file, force):
    """
    Reads defined type of data from file or cache
    :param data_type: key where the data is stored in cache
    :param file: relative path to data file
    :param force: if set to True, cache will be ignored
    :return: OrderedDict
    """
    if force or data_type not in _cache:
        _cache[data_type] = _read_csv(file)
    return _cache[data_type]


def get_highest_id(file_name):
    highest_id = 0
    all_rows = _read_csv(file_name)
    for row in all_rows:
        highest_id = int(row['id']) if int(row['id']) > highest_id else highest_id
    return str(highest_id)


def append_row(data: dict, file_name):
    new_row = []
    if file_name == './data/boards.csv':
        headers = BOARDS_HEADER
    elif file_name == './data/cards.csv':
        headers = CARDS_HEADER
    elif file_name == './data/statuses.csv':
        headers = STATUSES_HEADER
    else:
        return
    for header in headers:
        for key in data:
            if key == header:
                new_row.append(data[key])
                continue
    with open(file_name, 'a+') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(new_row)


def clear_cache():
    for k in list(_cache.keys()):
        _cache.pop(k)


def get_statuses(force=False):
    return _get_data('statuses', STATUSES_FILE, force)


def get_boards(force=False):
    return _get_data('boards', BOARDS_FILE, force)


def get_cards(force=False):
    return _get_data('cards', CARDS_FILE, force)
