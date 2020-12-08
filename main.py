from flask import Flask, render_template, url_for, request
from util import json_response

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


@app.route("/add-board", methods = ["POST"])
@json_response
def add_a_new_board():
    """
    Gets the board title from the (JSON) POST request and 
    writes it in server database (csv)
    """
    posted_data = request.json    
    if "title" in posted_data:        
        data_handler.create_new_board(posted_data["title"])
    else:
        return "Mangled data", 400
    # I don't think the above is a proper JSON server response with status: 400


def main():
    app.run(debug=True)

    # Serving the favicon
    with app.app_context():
        app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon/favicon.ico'))


if __name__ == '__main__':
    main()
