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
