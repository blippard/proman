from flask import Flask, render_template, url_for, request
from util import json_response, status_response, construct_default_reply

import data_handler

app = Flask(__name__)


@app.route("/")
def index():
    """
    This is a one-pager which shows all the boards and cards
    """
    return render_template('index.html')


@app.route("/get-boards")
@json_response
def get_boards():
    """
    All the boards
    """
    return data_handler.get_boards()


@app.route("/get-cards/<int:board_id>")
@json_response
def get_cards_for_board(board_id: int):
    """
    All cards that belongs to a board
    :param board_id: id of the parent board
    """
    return data_handler.get_cards_for_board(board_id)


@app.route("/get-board-statuses/<int:board_id>")
@json_response
def get_status(board_id: int):
    return data_handler.get_board_statuses(board_id)


@app.route("/add-card", methods=["POST"])
@status_response
def add_a_new_card():

    @construct_default_reply
    def basic_function(request_object):    
        posted_data = request_object.json        
        if "title" in posted_data:            
            return data_handler.create_new_card(posted_data)

    return basic_function(request_object=request)


@app.route("/rename-board", methods=["POST"])
@status_response
def rename_board():

    @construct_default_reply
    def basic_function(request_object):
        posted_data = request_object.json        
        if "title" in posted_data:  
            data_handler.rename_board(posted_data)
            return {}

    return basic_function(request_object=request)


@app.route("/rename-column", methods=["POST"])
@status_response
def rename_column():

    @construct_default_reply
    def basic_function(request_object):
        posted_data = request_object.json        
        if "title" in posted_data: 
            data_handler.rename_column(posted_data)
            return {}

    return basic_function(request_object=request)


# NOT YET
# @app.route("/rename-card", methods=["POST"])
# @json_response
# def rename_card():
#     posted_data = request.json
#     if "title" in posted_data:
#         data_handler.rename_card(posted_data)
#     else:
#         return "Mangled data", 400


@app.route("/add-board", methods=["POST"])
@status_response
def add_a_new_board():
    """
    Gets the board title from the (JSON) POST request and
    writes it in server database (csv)
    """
    @construct_default_reply
    def basic_function(request_object):
        posted_data = request_object.json
        if "title" in posted_data:
            return data_handler.createback_new_board(posted_data["title"])

    return basic_function(request_object=request)


@app.route("/delete-board/<int:board_id>", methods=["POST"])
@status_response
def delete_a_board(board_id):

    @construct_default_reply
    def basic_function(request_object):
        posted_data = request_object.json      
        try:
            posted_id = int(posted_data["id"])           
        except (ValueError, TypeError, KeyError):
            print("Failed in typecasting")
            return None
        else:
            if posted_id == board_id:
                try:                    
                    return_dict = data_handler.pop_from_list_board(board_id, force=False)
                except (TypeError, ValueError):
                    print("Failed in not finding id")
                    return None
                else:
                    return return_dict
            else:
                print("Failed in supplying proper JSON id")
                return None

    return basic_function(request_object=request)

@app.route('/registration', methods=['POST'])
@json_response
def registration():
    new_user = request.json['username']
    plain_text_password = request.json['password']
    confirm_password = request.json['confirmPassword']
    if plain_text_password == confirm_password:
        if data_handler.get_user(new_user):
            return 'Failure'
        data_handler.add_user(new_user, plain_text_password)
        return 'Success'


@app.route('/login', methods=['POST'])
@json_response
def login():    
    username = request.json['username']
    password = request.json['password']
    user = data_handler.get_user_for_login(username, password)
    if user:
        return user[0]
    else:
        return 'Failure'


@app.route("/update-card", methods=["POST"])
@status_response
def update_card():

    @construct_default_reply
    def basic_function(request_object):
        posted_data = request_object.json
        if "id" in posted_data:
            data_handler.update_cards(posted_data)
    
    return basic_function(request_object=request)

def main():
    app.run(debug=True)

    # Serving the favicon
    with app.app_context():
        app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon/favicon.ico'))


if __name__ == '__main__':
    main()
