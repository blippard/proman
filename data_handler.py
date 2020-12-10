import persistence
import csv
import bcrypt


def get_card_status(status_id):
    """
    Find the first status matching the given id
    :param status_id:
    :return: str
    """
    statuses = persistence.get_statuses(True)
    return next((status['title'] for status in statuses if status['id'] == str(status_id)), 'Unknown')


def get_boards():
    """
    Gather all boards
    :return:
    """
    all_boards = persistence.get_boards(force=True)
    for board in all_boards:
        temp_statuses = board['board_statuses'].split(',')
        for i, status in enumerate(temp_statuses):
            temp_statuses[i] = get_card_status(int(status))
        board['board_statuses'] = temp_statuses
    return all_boards


def get_cards_for_board(board_id):
    persistence.clear_cache()
    all_cards = persistence.get_cards()
    matching_cards = []
    for card in all_cards:
        if card['board_id'] == str(board_id):
            card['status_id'] = get_card_status(card['status_id'])  # Set textual status for the card
            matching_cards.append(card)
    return matching_cards


def get_board_statuses(boardId):
    persistence.clear_cache()
    all_boards = persistence.get_boards()
    all_statuses = persistence.get_statuses()
    matching_statuses = []
    for board in all_boards:
        if board['id'] == str(boardId):
            board_statuses = board['board_statuses'].split(',')
            for status in all_statuses:
                if status['id'] in board_statuses:
                    matching_statuses.append(status)
    return matching_statuses


def get_new_id_for_cards():
    card_id = len(persistence.get_cards()) + 1
    persistence.clear_cache()
    return card_id


def create_new_card(card_data):
    order = 0
    cards_dictionary = {'id': get_new_id_for_cards(),
                        'board_id': card_data['board_id'],
                        'title': card_data['title'],
                        'status_id': card_data['status_id'],
                        'order': order
                        }
    persistence.append_cards(cards_dictionary)
    return cards_dictionary


def get_new_id_for_boards():
    """
    Gets a new (valid) id for a board
    :return: int representing the next available ID
    """
    all_boards = get_boards()
    id_list = []
    for board in all_boards:
        try:
            new_id = int(board['id'])
        except (ValueError, TypeError):
            pass
        else:
            id_list.append(new_id)

    max_id = max(id_list)
    return max_id + 1


def createback_new_board(title):
    row_dict = {'id': str(get_new_id_for_boards()), 'title': title, 'board_statuses': '0,1,2,3'}
    persistence.append_boards(row_dict)
    return row_dict


def rename_board(board_data):
    id = board_data['board_id']
    new_title = board_data['title']
    persistence.rename_board(id, new_title)    


def rename_column(column_data):
    old_name = column_data['old-name']
    new_title = column_data['title']
    persistence.rename_column(old_name, new_title)    


# # NOT YET
# def rename_card(card_data):
#     card_id = card_data['card-id']
#     new_title = card_data['title']
#     persistence.rename_card(card_id, new_title)
#     return row_dict


def get_user(username):
    with open('./data/user.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] != 'id':
                if username == row[1]:
                    return row


def get_user_list():
    with open('./data/user.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        return list(csv_reader)


def generate_id():
    user_list = get_user_list()
    id = str(int(user_list[-1][0]) + 1)
    return id


def add_user(username, password):
    id = generate_id()
    with open('./data/user.csv', mode='a') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow([id, username, hash_password(password)])


def hash_password(plain_text_password: str):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_user_for_login(username, password):
    with open('./data/user.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[0] != 'id':
                if username == row[1]:
                    if verify_password(password, row[2]):
                        return row


def update_cards(card_update_data):
    cards = persistence.get_cards()
    for card in cards:
        if card['id'] == card_update_data['id']:
            card['status_id'] = card_update_data['status']
    all_cards_list = [list(card.values()) for card in cards]
    all_cards_list.insert(0, persistence.CARDS_HEADER)
    persistence.overwrite_csv(persistence.CARDS_FILE, all_cards_list)


def pop_from_list_board(board_id, force=False):
    all_boards = persistence.get_boards(force=True)
    id_list = [row["id"] for row in all_boards]
    try:
        the_index = id_list.index(str(board_id))
    except (TypeError, ValueError):
        raise
    
    del id_list
    if force:        
        # we just delete from boards DB and not from other DBs
        pass
    else:        
        remove_all_cards_of_board(board_id)

    row_dict = all_boards.pop(the_index)    
    persistence.write_boards(all_boards)

    return row_dict


def remove_all_cards_of_board(board_id):
    all_cards = persistence.get_cards(force=True)    
    new_cards = [row for row in all_cards if row["board_id"] != str(board_id)]
    del all_cards
    persistence.write_cards(new_cards)
            

def add_status_to_board(board_id, column_title_json):
    column_title = column_title_json['columnTitle']
    boards = persistence.get_boards()
    if not persistence.check_if_status_exists(column_title):
        status_id = str(int(persistence.get_highest_id('./data/statuses.csv')) + 1)
        persistence.append_row({'id' : status_id,
                                'title' : column_title},
                               './data/statuses.csv')
    else:
        status_id = persistence.get_status_id(column_title)
    for board in boards:
        if int(board['id']) == int(board_id):
            board['board_statuses'] += f',{status_id}'
    persistence._write_csv('./data/boards.csv', 'boards', boards)
