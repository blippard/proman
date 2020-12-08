// It uses data_handler.js to visualize elements
import { dataHandler } from "./data_handler.js";

export let dom = {
  init: function () {
    // This function should run once, when the page is loaded.
    const newBoardBtn = document.querySelector(".add-board-btn");
    newBoardBtn.addEventListener("click", (event) => {
      event.preventDefault();
      let inputTitle = prompt("What is the title of the new board?");
      if (!(inputTitle === "") && (inputTitle)) {
        dataHandler.createNewBoard(inputTitle, (response) => {
          //if (response.json() !== "") {
          location.reload();
          //}
          // upon receiving a response, we refresh the page to update display
        });
      }
    });

  },
  loadBoards: function () {
    // retrieves boards and makes showBoards called
    dataHandler.getBoards(function (boards) {
      dom.showBoards(boards);
    });
  },
  showBoards: function (boards) {
    // shows boards appending them to #boards div
    // it adds necessary event listeners for (each board) also

    let boardList = "";

    for (let board of boards) {
      // can change the HTML container types (not necessarily divs) later
      boardList += `
                <div class="board">
                    <div class="board-header" id-of-board="${board.id}">${board.title}</div>
                    <button board-id="${board.id}">New Card</button>
                </div>
            `;
    }

    const outerHtml = `
            <div class="board-container">
                ${boardList}
            </div>
        `;


        let boardsContainer = document.querySelector('#boards');
        boardsContainer.insertAdjacentHTML("beforeend", outerHtml);
    },
    loadCards: function (boardId) {
        // retrieves cards and makes showCards called
      fetch(`/get-boards/${boardId}`).then((response) => response.json()).then((data) => {
        console.log(data);
      })
    },
    showCards: function (cards) {
        // shows the cards of a board
        // it adds necessary event listeners also
      for (let card of cards) {
        // can change the HTML container types (not necessarily divs) later
        console.log(card);
        let cardDiv = document.createElement('div');
        cardDiv.setAttribute('')
      }

    },
    // here comes more features
    newCardEventListener: function () {
      let newCardButtons = document.querySelectorAll("button[board-id]");
      for (let button of newCardButtons) {
        button.addEventListener('click', function () {
          let boardId = button.getAttribute('board-id');
          let cardName = prompt("Name your card");
          if (!(cardName === "") && (cardName)) {
            // createNewCard: function (cardTitle, boardId, statusId, callback)
            dataHandler.createNewCard(cardName, boardId, '0')
          }
        })
      }
    },

    getAllCards: function () {
      fetch('/get-boards').then((response) => response.json()).then((data) => {
        for (let board of data) {
          fetch(`/get-cards/${board.id}`)
              .then((response) => response.json())
              .then((cardData) => {
                this.showCards(cardData);
              });
          }
      });
    }
};
