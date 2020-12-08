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
                    <div class="board-header">${board.title}</div>
                </div>
            `;
    }

    const outerHtml = `
            <div class="board-container">
                ${boardList}
            </div>
        `;

    let boardsContainer = document.querySelector("#boards");
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
