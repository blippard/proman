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


def _write_csv(file_name, data_type, list_of_dict):
    """
    Overwrites the content of a .csv file with provided data (a non-empty list)
    :param file_name: relative path to file
    :param data_type: a key ('boards', 'statuses') to help determine the 
      header for the .csv (this is a canonical order for the keys in the dicts
      Each dict could have its keys sorted differently - by insertion order -)
    :param list_of_dict: list of dictionaries (each dictionary 
      is a row in the .csv) -> function assumes all dicts
      have the same keys and these correspond to the headers of given data_type
    """
    with open(file_name, 'w', newline='') as csvfile:
        if len(list_of_dict) > 0:
            if data_type == 'boards':
                my_fieldnames = BOARDS_HEADER
            elif data_type == 'cards':
                my_fieldnames = CARDS_HEADER
            elif data_type == 'statuses':
                my_fieldnames = STATUSES_HEADER
            else:
                print('Wrong data type!')
                return
                
            writer = csv.DictWriter(csvfile, fieldnames=my_fieldnames)
            writer.writeheader()    # writes the first row of the .csv (the keys in my_fieldnames)
            writer.writerows(list_of_dict)


def get_highest_id(file_name):
    highest_id = 0
    all_rows = _read_csv(file_name)
    for row in all_rows:
        highest_id = int(row['id']) if int(row['id']) > highest_id else highest_id
    return str(highest_id)


def check_if_status_exists(title):
    all_rows = _read_csv(STATUSES_FILE)
    for row in all_rows:
        if row['title'] == title:
            return True
    return False


def get_status_id(title):
    all_rows = _read_csv(STATUSES_FILE)
    for row in all_rows:
        if row['title'] == title:
            return row['id']


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
        values_list = [ row[field] if field in row else "" for field in my_fieldnames ]

        writer = csv.writer(csvfile, quotechar='"')
        writer.writerow(values_list)


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


def get_data_from_csv(filename):
    with open(filename, newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_list = list(csv_reader)
        csv_file.close()
    return csv_list


def _edit_csv(file_name, id, new_name):
    csv_list = get_data_from_csv(file_name)
    for row in csv_list:
        if row[0] == id:
            row[1] = new_name
    with open(file_name, 'w', newline='') as writer:
        data = csv.writer(writer, delimiter=',')
        for row in csv_list:
            data.writerow(row)


def _edit_status_csv(file_name, old_name, new_name):
    csv_list = get_data_from_csv(file_name)
    for row in csv_list:
        if row[1] == old_name:
            row[1] = new_name
    with open(file_name, 'w', newline='') as writer:
        data = csv.writer(writer, delimiter=',')
        for row in csv_list:
            data.writerow(row)


def _edit_card_csv(file_name, card_id, new_name):
    csv_list = get_data_from_csv(file_name)
    for row in csv_list:
        if row[0] == card_id:
            row[2] = new_name
    with open(file_name, 'w', newline='') as writer:
        data = csv.writer(writer, delimiter=',')
        for row in csv_list:
            data.writerow(row)


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


def rename_board(id, new_name):
    _edit_csv(BOARDS_FILE, id, new_name)


def rename_column(old_name, new_name):
    _edit_status_csv(STATUSES_FILE, old_name, new_name)


def write_boards(list_of_dict):
    _write_csv(BOARDS_FILE, 'boards', list_of_dict)


def write_cards(list_of_dict):
    _write_csv(CARDS_FILE, 'cards', list_of_dict)

# NOT YET
# def rename_card(card_id, new_name):
#     _edit_card_csv(CARDS_FILE, card_id, new_name)


def overwrite_csv(file_path, new_data):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(new_data)
