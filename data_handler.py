import persistence
import csv


def get_card_status(status_id):
    """
    Find the first status matching the given id
    :param status_id:
    :return: str
    """
    statuses = persistence.get_statuses()
    return next((status['title'] for status in statuses if status['id'] == str(status_id)), 'Unknown')


def get_boards():
    """
    Gather all boards
    :return:
    """
    return persistence.get_boards(force=True)


def get_cards_for_board(board_id):
    persistence.clear_cache()
    all_cards = persistence.get_cards()
    matching_cards = []
    for card in all_cards:
        if card['board_id'] == str(board_id):
            card['status_id'] = get_card_status(card['status_id'])  # Set textual status for the card
            matching_cards.append(card)
    return matching_cards


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
        csv_writer.writerow([id, username, password])


