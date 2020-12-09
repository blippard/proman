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


def _append_csv(file_name, data_type, row):
    """
    Appends the content of a .csv file with a single row (a dict)
    :param file_name: relative path to file
    :param data_type: a key ('boards', 'statuses' etc.) to help determine the
      header for the .csv (the canonical order of keys)
    :param row: a SINGLE dictionary with keys the sames as header for data_type
    """
    with open(file_name, 'a', newline='') as csvfile:
        if data_type == 'boards':
            my_fieldnames = BOARDS_HEADER
        elif data_type == 'cards':
            my_fieldnames = CARDS_HEADER
        elif data_type == 'statuses':
            my_fieldnames = STATUSES_HEADER
        else:
            print('Wrong data type!')
            return

        # turn the dictionary into a sorted list of values corresponding to the canonical
        # ordering of the dictionary keys [this order is given by the header (my_fieldnames)]
        values_list = [row[field] if field in row else "" for field in my_fieldnames]

        writer = csv.writer(csvfile)
        writer.writerow(values_list)


def clear_cache():
    for k in list(_cache.keys()):
        _cache.pop(k)


def get_statuses(force=False):
    return _get_data('statuses', STATUSES_FILE, force)


def get_boards(force=False):
    return _get_data('boards', BOARDS_FILE, force)


def get_cards(force=False):
    return _get_data('cards', CARDS_FILE, force)


def append_cards(board_dict):
    _append_csv(CARDS_FILE, 'cards', board_dict)


def append_boards(board_dict):
    _append_csv(BOARDS_FILE, 'boards', board_dict)
