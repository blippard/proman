// It uses data_handler.js to visualize elements
import {dataHandler} from "./data_handler.js";

export let dom = {
    init: function () {
        let registrationButton = document.getElementById('registration-button');
        let registerSubmit = document.getElementById('reg-button')
        registrationButton.addEventListener('click', () => {
            let registrationContainer = document.getElementById('registration-container');
            let menuButton = document.getElementById('menu');
            let boards = document.getElementById('boards');
            registrationContainer.style.display = 'flex';
            menuButton.style.display = 'none';
            boards.style.display = 'none';
        });
        registerSubmit.addEventListener('click', () => {
            let registrationContainer = document.getElementById('registration-container')
            let menuButton = document.getElementById('menu');
            let boards = document.getElementById('boards');
            let username = document.getElementById('username');
            let password = document.getElementById('password');
            let confirmPassword = document.getElementById('confirm_password');
            this.postdata('http://127.0.0.1:5000/registration', {
                username: username.value,
                password: password.value,
                confirmPassword: confirmPassword.value
            }).then((response) => {
                if (response === 'Failure') {
                    alert('Username is already in use!')
                } else {
                    registrationContainer.style.display = 'none';
                    menuButton.style.display = 'block';
                    boards.style.display = 'block';
                }
            })
        });
        // This function should run once, when the page is loaded.
    },
    postdata: async function (url = '', data) {
        const response = await fetch(url,{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }
        )
        return response.json()
    },
    loadBoards: function () {
        // retrieves boards and makes showBoards called
        dataHandler.getBoards(function (boards) {
            dom.showBoards(boards);
        });
    },
    showBoards: function (boards) {
        // shows boards appending them to #boards div
        // it adds necessary event listeners also

        let boardList = '';

        for (let board of boards) {
            boardList += `
                <li>${board.title}</li>
            `;
        }

        const outerHtml = `
            <ul class="board-container">
                ${boardList}
            </ul>
        `;

        let boardsContainer = document.querySelector('#boards');
        boardsContainer.insertAdjacentHTML("beforeend", outerHtml);
    },
    loadCards: function (boardId) {
        // retrieves cards and makes showCards called
    },
    showCards: function (cards) {
        // shows the cards of a board
        // it adds necessary event listeners also
    },
    // here comes more features
};
