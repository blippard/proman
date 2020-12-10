// It uses data_handler.js to visualize elements
import { dataHandler } from "./data_handler.js";

export let dom = {
    init: function () {
        // This function should run once, when the page is loaded.
    },
    loadBoards: function () {
        // retrieves boards and makes showBoards called
        this.removeAllBoardElements();
        dataHandler.getBoards(function(boards){
            dom.showBoards(boards);
            for (let board of boards) {
                dom.loadCards(board.id);
            }
        });
    },
    showBoards: function (boards) {
        // shows boards appending them to #boards div
        // it adds necessary event listeners also

        let boardList = '';

        for(let board of boards){
            let columnlist = '';
            for (let column of board.board_statuses){
                columnlist += `
                <div class="col border border-dark p-0 ${dataHandler.camelize(column)}${board.id}">
                    <div class="'card-column-title text-center border-bottom border-dark mb-2'">${column}</div>
                </div>
                `
            }
            boardList += `
                <section class="board col mb-5 border border-dark" id="wholeBoard${board.id}">
                    <div class="board-header">
                        <span class="board-title">${board.title}</span>
                        <button class="btn btn-dark add-column" data-toggle="modal" data-target="#submitModal" data-board-id="${board.id}">Add column</button>
                        <button class="btn btn-dark float-right" type="button" data-toggle="collapse" data-target="#board${board.id}" aria-expanded="false" aria-controls="board${board.id}"></button>
                    </div>
                    <div class="row collapse" id="board${board.id}">
                        ${columnlist}
                    </div>
                </section>
            `;
        }

        const outerHtml = `
            <div class="board-container">
                ${boardList}
            </div>
        `;

        let boardsContainer = document.querySelector('#boards');
        boardsContainer.insertAdjacentHTML("beforeend", outerHtml);
        let addColumnButtons = document.querySelectorAll('.add-column');
        for (let button of addColumnButtons) {
            button.addEventListener('click', (event) => this.initAddColumn(event));
        }
    },
    loadCards: function (boardId) {
        // retrieves cards and makes showCards called
        dataHandler.getCardsByBoardId(boardId,function(cards){
            dom.showCards(cards);
        })
    },
    showCards: function (cards) {
        // shows the cards of a board
        // it adds necessary event listeners also
        for (let card of cards){
            let board = document.querySelector(`#board${card.board_id}`);
            if (`board${card.board_id}` == `${board.id}`) {
                let cardColumn = board.querySelector(`.${dataHandler.camelize(card.status_id)}${card.board_id}`);
                let cardToAdd = `
                    <div class="card mx-2 mb-2 border border-dark text-center">
                        ${card.title}
                    </div>
                `;
                cardColumn.insertAdjacentHTML('beforeend', cardToAdd);
            }
        }
    },
    // here comes more features
    removeAllBoardElements: function () {
        let allBoards = document.querySelector('#boards');
        if (allBoards) {
            allBoards.innerHTML = '';
        }
    },
    initAddColumn: function (event) {
        let boardSection = event.target.parentNode.parentNode
        if (boardSection.tagName === 'SECTION' && boardSection.classList.contains('board')) {
            console.log(event.target.dataset.boardId);
        }
    }
};
