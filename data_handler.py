import persistence


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


def update_cards(card_update_data):
    cards = persistence.get_cards()
    for card in cards:
        if card['id'] == card_update_data['id']:
            card['status_id'] = card_update_data['status']
    all_cards_list = [list(card.values()) for card in cards]
    all_cards_list.insert(0, persistence.CARDS_HEADER)
    persistence.overwrite_csv(persistence.CARDS_FILE, all_cards_list)

# if __name__ == '__main__':
#     pass
