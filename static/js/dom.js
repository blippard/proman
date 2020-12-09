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
                <div class="board" data-id-of-board="${board.id}">
                    <div class="board-header">
                      <span>${board.title}</span>
                      <button class="remove-board">Delete Board 🗑️</button>
                    </div>
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

    document.querySelectorAll(".remove-board").forEach((item) => {
      item.addEventListener("click", (event) => {
        // the .board is the grandparent of the .remove-board (the parent is .board-header)
        this.handleRemoveBoardClick(item.parentNode.parentNode, event);
      });
    });
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
  createNewChildBoard: function (boardDict) {
    const boardInnerContainer = document.querySelector(".board-container");
    let childHTMLText = `
                <div class="board" data-id-of-board="${boardDict.id}">
                    <div class="board-header">
                      <span>${boardDict.title}</span>
                      <button class="remove-board">Delete Board 🗑️</button>
                    </div>
                </div>
            `;
    boardInnerContainer.insertAdjacentHTML("beforeend", childHTMLText);
    let newRemoveBoardBtn = boardInnerContainer.lastElementChild.querySelector(
      ".remove-board"
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
    dataHandler.deleteBoard(boardNode.dataset.idOfBoard, (jsonResponse) => {
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
