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

    let boardsSupraContainer = document.querySelector("#boards");
    boardsSupraContainer.insertAdjacentHTML("beforeend", outerHtml);
  },
  loadCards: function (boardId) {
    // retrieves cards and makes showCards called
  },
  showCards: function (cards) {
    // shows the cards of a board
    // it adds necessary event listeners also
  },
  // here comes more features
  handleAddBoardClick: function (clickEvent) {
    clickEvent.preventDefault();
    let inputTitle = prompt("What is the title of the new board?");
    if (!(inputTitle === "") && inputTitle) {
      dataHandler.createNewBoard(inputTitle, (jsonResponse) => {
        if (jsonResponse.title) {
          this.createNewChildBoard(jsonResponse.title);
        } else {
          window.alert(
            "Could not get reply from server. Please wait and try again later."
          );
          // could maybe add a child that lives only until next _data update (next showBoards call)
        }
      });
    }
  },
  createNewChildBoard: function (boardTitle) {
    const boardInnerContainer = document.querySelector(".board-container");
    let childHTMLText = `
                <div class="board">
                    <div class="board-header">${boardTitle}</div>
                </div>
            `;
    boardInnerContainer.insertAdjacentHTML("beforeend", childHTMLText);
  },
};
