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


def create_new_board(title):
    row_dict = {'id': get_new_id_for_boards(), 'title': title}
    persistence.append_boards(row_dict)


def get_new_id_for_cards(board_id):
    return len(get_cards_for_board(board_id)) + 1


def create_new_card(card_data):
    order = 0
    cards_dictionary = {'id': get_new_id_for_cards(card_data['board_id']),
                'board_id': card_data['board_id'],
                'title': card_data['title'],
                'status_id': card_data['status_id'],
                'order': order
                }
    persistence.append_cards(cards_dictionary)


# for testing and debugging
# if __name__ == "__main__":
#     print(len(get_cards_for_board(1)))
