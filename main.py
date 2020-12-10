from flask import Flask, render_template, url_for, request, Response
from util import json_response, status_response

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
    reply = {}
    if ('Content-Type' in request.headers) and (request.headers['Content-Type'] == 'application/json'):
        posted_data = request.json        
        if "title" in posted_data:
            data_handler.create_new_card(posted_data)
            # reply["json_data"] = {} # need to return something in the reply here        
            # return reply
        else:
            reply["json_data"] = {"STATUS_TEXT": "Mangled data"}
            reply["status"] = 400
            return reply
    else:
        reply["json_data"] = {"STATUS_TEXT": "Unsupported media type (expecting application/json)"}
        reply["status"] = 415
        return reply


@app.route("/add-board", methods=["POST"])
@status_response
def add_a_new_board():
    """
    Gets the board title from the (JSON) POST request and
    writes it in server database (csv)
    """
    reply = {}
    if ('Content-Type' in request.headers) and (request.headers['Content-Type'] == 'application/json'):
        posted_data = request.json        
        if "title" in posted_data:
            reply["json_data"] = data_handler.createback_new_board(posted_data["title"])
            return reply
        else:
            reply["json_data"] = {"STATUS_TEXT": "Mangled data"}
            reply["status"] = 400
            return reply
    else:
        reply["json_data"] = {"STATUS_TEXT": "Unsupported media type (expecting application/json)"}
        reply["status"] = 415
        return reply

   

def main():
    app.run(debug=True)

    # Serving the favicon
    with app.app_context():
        app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon/favicon.ico'))


if __name__ == '__main__':
    main()
