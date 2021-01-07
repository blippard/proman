import connection as db
# import csv    # this shouldn't have been imported here even when using CSV, rather in 'persistence'
import bcrypt


def get_card_status(status_id):
    """
    Find the first status matching the given id
    :param status_id:
    :return: str
    """
    statuses = get_statuses()
    return next((status['title'] for status in statuses if status['id'] == status_id), 'Unknown')


def get_boards():
    """
    Gather all boards
    :return:
    """
    all_boards = db.get_data_from_table('board')
    # TODO: needs board_to_status refactor 
    # temp_statuses logic could be done in SQL (get a list of status_ids and turn it into status_titles)
    for board in all_boards:
        temp_statuses = db.get_sorted_inner_join_where_table2_column_has_value_and_order_by_table1_column(
            table1_name='status', 
            table2_name='board_to_status', 
            table2_column='board_id', 
            table2_column_value=board['id'],
            table1_keycol='id',
            table2_keycol='status_id',
            table1_column_to_order='id'
        )
        
        for i, status in enumerate(temp_statuses):
            
            temp_statuses[i] = get_card_status(int(status['id']))   # changed, since temp_statuses is now a list of 
            #                                                       # status dicts rather than a list of status ids
        board['board_statuses'] = temp_statuses
    return all_boards


def get_cards_for_board(some_board_id: int):
    
    result = db.get_data_by_kw_value_pair_from_table({'board_id': some_board_id}, 'card')
    for card in result:
        card['status_id'] = get_card_status(int(card['status_id']))
    return result


def get_board_statuses(some_board_id: int):
    return db.get_sorted_inner_join_where_table2_column_has_value_and_order_by_table1_column(
        table1_name="status", 
        table2_name="board_to_status",
        table2_column="board_id",
        table2_column_value=some_board_id,
        table1_keycol="id",
        table2_keycol="status_id",
        table1_column_to_order="id"
    )


def get_new_id_for_cards():
    card_id = db.get_max_serial_from_table('card') + 1    
    return card_id


def create_new_card(card_data):
    order = 0
    cards_dictionary = {'id': get_new_id_for_cards(),
                        'board_id': card_data['board_id'],
                        'title': card_data['title'],
                        'status_id': card_data['status_id'],
                        'order': order
                        }
    append_cards(cards_dictionary)
    return cards_dictionary


def get_new_id_for_boards():
    """
    Gets a new (valid) id for a board
    :return: int representing the next available ID
    """
    max_id = db.get_max_serial_from_table('board')
    return max_id + 1


def createback_new_board(title):
    new_id = get_new_id_for_boards()
    row_dict = {'id': new_id, 'title': title, 'user_id': 0}   # default behavior, change user_id here later
    append_boards(row_dict)
    for i in range(0, 3+1):  # default statuses for board (the previous board_statuses 0,1,2,3)
        status_connection_dict = {'board_id': new_id, 'status_id': i}
        db.append_row_in_table(status_connection_dict, 'board_to_status')
    # TODO: refactor the JS need for this next key, if any at all
    row_dict['board_statuses'] = '0,1,2,3'  # kept for compatibility purposes when returning back
    return row_dict


def rename_board(board_data):
    # maybe not use board_data, but 2 params: board_id and new_title
    board_id = board_data['board_id']
    new_title = board_data['title']
    db.update_data_in_table({'id': board_id, 'title': new_title}, 'board')


# TODO: query for existing titles and assign ids accordingly
#
def rename_column(column_data): 
    old_name = column_data['old-name']
    new_title = column_data['title']    # should also get in column_data the board_id where we rename (as some_board_id)

#     status_dict = get_single_row_by_kw_value_pair_from_table({'title': old_name},'status')    
#     old_status_id = status_dict['id']
#     new_status_id = get_max_serial_from_table('status') + 1
#     append_row_in_table({'id': new_status_id, 'title': new_title}, 'status')
#     update_data_in_table(
#         some_dict={'board_id': some_board_id, 'status_id': new_status_id},
#         table_name='board_to_status', 
#         id_val=(some_board_id, new_status_id) # this primary key is a pair of values, will need to use something else
#     )   
    pass


# # NOT YET
# def rename_card(card_data):
#     card_id = card_data['card-id']
#     new_title = card_data['title']
#     persistence.rename_card(card_id, new_title)
#     return row_dict


def get_user(some_username):
    return db.get_single_row_by_kw_value_pair_from_table({'username': some_username}, 'user')


def generate_user_id():
    max_id = db.get_max_serial_from_table('user')
    return max_id + 1


def add_user(new_username, new_plain_password):
    new_user_id = generate_user_id()
    user_dict = {
        'id': new_user_id, 
        'username': new_username, 
        'password': hash_password(new_plain_password)
        }
    db.append_row_in_table(user_dict, 'user')


def hash_password(plain_text_password: str):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_user_for_login(some_username, plaintext_password):
    user_dict = db.get_single_row_by_kw_value_pair_from_table({'username': some_username}, 'user')
    hashed_password = user_dict['password']
    if verify_password(plaintext_password, hashed_password):
        return user_dict
    else:
        return None


def update_cards(card_update_data):
    card_update_data['status_id'] = card_update_data['status']  # this is a workaround for compatibility!
    #                                                           # JSON dictionary data structure should match table!
    db.update_data_in_table(card_update_data, 'card')    


def pop_from_list_board(board_id, force=False):
    # TODO: handle board_id not-found errors and raise ValueError as before
    row_dict = db.get_single_row_by_kw_value_pair_from_table({'id': board_id}, 'board')
    db.delete_row_with_id(board_id, 'board')
    # due to ON DELETE CASCADE there is no need for remove_all_cards_of_board
    # ... or 'force' boolean argument, for that matter

    return row_dict

          
def add_status_to_board(board_id, column_title_json):
    column_title = column_title_json['columnTitle']    
    result_dict = db.get_single_row_by_kw_value_pair_from_table({'title': column_title}, 'status')
    if 'id' not in result_dict:
        status_id = db.get_max_serial_from_table('status') + 1
        db.append_row_in_table({'id': status_id,
                                'title': column_title},
                               'status')
    else:        
        status_id = result_dict['id']
    status_connection_dict = {'board_id': board_id, 'status_id': status_id}
    db.append_row_in_table(status_connection_dict, 'board_to_status')


def get_statuses():
    return db.get_data_from_table('status')


def get_simple_boards():
    return db.get_data_from_table('board')


def get_cards():
    return db.get_data_from_table('card')


def get_users():
    return db.get_data_from_table('user')


def append_boards(board_dict):
    db.append_row_in_table(board_dict, table_name='board')


def append_cards(card_dict):
    db.append_row_in_table(card_dict, table_name='card')


if __name__ == "__main__":      # for testing purposes
    print(db.column_names_dict)    
    append_boards({'id': 21, 'title': "test"})
    print(get_boards())
    pop_from_list_board(21)
    print(get_boards())
    print(get_cards_for_board(2))