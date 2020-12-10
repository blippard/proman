// It uses data_handler.js to visualize elements
import { dataHandler } from "./data_handler.js";

export let dom = {
    init: function () {
        // This function should run once, when the page is loaded.
        const newBoardBtn = document.querySelector(".add-board-btn");
        newBoardBtn.addEventListener("click", (event) => {
            this.handleAddBoardClick(event);
        });
    },
    loadBoards: function () {
        // retrieves boards and makes showBoards called
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

    let boardList = "";

        for (let board of boards) {
            boardList += `
                <section class="board col mb-5 border border-dark">
                    <div class="board-header">
                        <span class="board-title">${board.title}</span>                        
                        <button class="new-card-btn" board-id="${board.id}">New Card</button>
                        <button class="remove-board-btn">Delete Board 🗑️</button>
                        <button class="btn btn-dark float-right" type="button" data-toggle="collapse" data-target="#board${board.id}" aria-expanded="false" aria-controls="board${board.id}">
                        </button>
                    </div>
                    <div class="row collapse" id="board${board.id}">
                        
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

        this.addCardEventListener();
        document.querySelectorAll(".remove-board-btn").forEach((item) => {
          item.addEventListener("click", (event) => {
            // the .board is the grandparent of the .remove-board-btn (the parent is .board-header)
            this.handleRemoveBoardClick(item.parentNode.parentNode, event);
          });
        });
        },
    addCardEventListener: function ()  {
        let newCardBtns = document.querySelectorAll('.new-card-btn');

        for (let cardBtn of newCardBtns) {
            let boardId = cardBtn.getAttribute('board-id');
            cardBtn.addEventListener('click', function () {
                // let cardTitle = prompt("Please add a title");
                let cardForm = `
                <form>
                <input type="text" name="title">
                <select name="status">
                    <option value="0">New</option>
                    <option value="1">In Progress</option>
                    <option value="2">Testing</option>
                    <option value="3">Done</option>
                </select>
                <input type="submit" id="new-card-submit">
                </form>
                `
                cardBtn.insertAdjacentHTML("afterend", cardForm);

                let form = document.querySelector('form')
                    form.addEventListener('submit', event => {
                        const formData = new FormData(event.target)
                        dataHandler.createNewCard(formData.get('title'), boardId, formData.get('status'));
                    })
            })
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
                if (!board.querySelector(`.${dataHandler.camelize(card.status_id)}${card.board_id}`)) {
                    let createCardColumn = document.createElement('div');
                    let createColumnTitle = document.createElement('div');
                    createCardColumn.setAttribute('class', `col border border-dark p-0 ${dataHandler.camelize(card.status_id)}${card.board_id}`);
                    createColumnTitle.setAttribute('class', 'card-column-title text-center border-bottom border-dark mb-2');
                    createColumnTitle.innerText = `${card.status_id}`;
                    createCardColumn.appendChild(createColumnTitle);
                    board.appendChild(createCardColumn);
                }
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
    handleAddBoardClick: function (clickEvent) {
      clickEvent.preventDefault();
      let inputTitle = prompt("What is the title of the new board?");
      if (!(inputTitle === "") && inputTitle) {
        dataHandler.createNewBoard(inputTitle, (jsonResponse) => {
          if (jsonResponse.title && jsonResponse.id) {
            this.createNewChildBoard(jsonResponse);
          } else {
            window.alert(
              "Could not get reply from server. Please wait and try again later."
            );
            // could maybe add a child that lives only until next _data update (next showBoards call)
          }
        });
      }
    },
  createNewChildBoard: function (board) {
    const boardInnerContainer = document.querySelector(".board-container");
    let childHTMLText = `
              <section class="board col mb-5 border border-dark">
                <div class="board-header">
                    <span class="board-title">${board.title}</span>                    
                    <button class="new-card-btn" board-id="${board.id}">New Card</button>
                    <button class="remove-board-btn">Delete Board 🗑️</button>
                    <button class="btn btn-dark float-right" type="button" data-toggle="collapse" data-target="#board${board.id}" aria-expanded="false" aria-controls="board${board.id}">
                    </button>
                </div>
                <div class="row collapse" id="board${board.id}">
                    
                </div>
              </section>
            `;
    boardInnerContainer.insertAdjacentHTML("beforeend", childHTMLText);
    let newRemoveBoardBtn = boardInnerContainer.lastElementChild.querySelector(
      ".remove-board-btn"
    );
    newRemoveBoardBtn.addEventListener("click", (event) => {
      this.handleRemoveBoardClick(
        newRemoveBoardBtn.parentNode.parentNode,
        event
      );
    });
  },
  handleRemoveBoardClick: function (boardNode, clickEvent) {
    // boardNode is the node in the DOM tree corresponding to a board HTML element
    // and, thus, element and node are interchangeable for almost all purposes
    clickEvent.preventDefault();
    dataHandler.deleteBoard(boardNode.id, (jsonResponse) => {
      if (!jsonResponse.success) {
        window.alert(
          "Could not get reply from server. Will delete only temporarily!"
        );
      }
    });
    // window.alert(`Deleted board with id=${boardNode.dataset.idOfBoard}`)
    boardNode.remove(); // this will remove all children of the node as well
  },
};
