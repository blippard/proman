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


@app.route('/registration', methods=['POST'])
@json_response
def registration():
    if request.method == 'POST':
        print(request.json)
        new_user = request.json['username']
        plain_text_password = request.json['password']
        confirm_password = request.json['confirmPassword']
        if plain_text_password == confirm_password:
            if data_handler.get_user(new_user):
                return 'Failure'
            data_handler.add_user(new_user, plain_text_password)
            return 'Success'


def main():
    app.run(debug=True)

    # Serving the favicon
    with app.app_context():
        app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon/favicon.ico'))


if __name__ == '__main__':
    main()
