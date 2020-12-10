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

        let boardList = '';

        for (let board of boards) {
            boardList += `
                <section class="board col mb-5 border border-dark">
                    <div class="board-header">
                        <span class="board-title">${board.title}</span>
                        <button class="btn btn-dark float-right" type="button" data-toggle="collapse" data-target="#board${board.id}" aria-expanded="false" aria-controls="board${board.id}"></button>
                        <button class="new-card-btn" board-id="${board.id}">New Card</button>
                        <button class="rename-board-btn" board-id="${board.id}" board-title="${board.title}">Rename Board</button>
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
        this.newNameBoardEventListener();
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
                <input type="submit" id="new-card-submit" value="Save">
                </form>
                `
                cardBtn.insertAdjacentHTML("afterend", cardForm);

                let form = document.querySelector('form')
                    form.addEventListener('submit', event => {
                        event.preventDefault();
                        const formData = new FormData(event.target)
                        const formSheet = document.querySelector('form');
                        dataHandler.createNewCard(formData.get('title'), boardId, formData.get('status'));
                        formSheet.remove();
                        dom.loadLatestCards(boardId);
                    })
            })
        }

    },

        newNameBoardEventListener: function ()  {
        let renameBoardBtn = document.querySelectorAll('.rename-board-btn');
        for (let boardBtn of renameBoardBtn) {
            let boardId = boardBtn.getAttribute('board-id');
            let boardTitle = boardBtn.getAttribute('board-title');
            boardBtn.addEventListener('click', function () {
                let cardForm = `
                <form>
                <input type="text" name="title" placeholder="${boardTitle}" value="${boardTitle}">
                <input type="submit" id="new-board-name-submit" value="Save">
                </form>
                `
                boardBtn.insertAdjacentHTML("afterend", cardForm);
                let form = document.querySelector('form')
                    form.addEventListener('submit', event => {
                        const formData = new FormData(event.target)
                        dataHandler.renameBoard(boardId, formData.get('title'));
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
    loadLatestCards: function (boardId) {
        // retrieves cards and makes showCards called
        dataHandler.getLatestCardsByBoardId(boardId,function(cards){
            dom.showCard(cards);
        })
    },
    showCard: function (card) {
        // shows the cards of a board
        // it adds necessary event listeners also
            let board = document.querySelector(`#board${card.board_id}`);
            if (`board${card.board_id}` == `${board.id}`) {
                if (!board.querySelector(`.${dataHandler.camelize(card.status_id)}${card.board_id}`)) {
                    let createCardColumn = document.createElement('div');
                    let createColumnTitle = document.createElement('div');
                    createCardColumn.setAttribute('class', `col border border-dark p-0 ${dataHandler.camelize(card.status_id)}${card.board_id}`);
                    createCardColumn.setAttribute('status', `${dataHandler.camelize(card.status_id)}`)
                    createColumnTitle.setAttribute('class', 'card-column-title text-center border-bottom border-dark mb-2');
                    createColumnTitle.innerText = `${card.status_id}`;
                    createCardColumn.appendChild(createColumnTitle);
                    board.appendChild(createCardColumn);
                }
                let cardColumn = board.querySelector(`.${dataHandler.camelize(card.status_id)}${card.board_id}`);
                let cardToAdd = `
                    <div id="${card.id}" draggable="true" class="${dataHandler.camelize(card.status_id)}" card="true">
                        ${card.title}
                    </div>
                `;
                cardColumn.insertAdjacentHTML('beforeend', cardToAdd);
            }

        this.createDropZone();
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
                    createCardColumn.setAttribute('status', `${dataHandler.camelize(card.status_id)}`)
                    createColumnTitle.setAttribute('class', 'card-column-title text-center border-bottom border-dark mb-2');
                    createColumnTitle.innerText = `${card.status_id}`;
                    createCardColumn.appendChild(createColumnTitle);
                    board.appendChild(createCardColumn);
                    createColumnTitle.addEventListener("click", function () {
                        let oldName = `${card.status_id}`;
                        let columnTitle = `${card.status_id}`;
                        let addName = `
                            <form>
                            <input type="text" name="title" placeholder="${columnTitle}" value="${columnTitle}">
                            <input type="submit" id="new-board-name-submit" value="Save">
                            </form>
                            `
                        createColumnTitle.insertAdjacentHTML("afterend", addName);
                        let form = document.querySelector('form')
                        form.addEventListener('submit', event => {
                            const formData = new FormData(event.target)
                            dataHandler.renameColumn(oldName, formData.get('title'));
                        })
                    });
                }
                let cardColumn = board.querySelector(`.${dataHandler.camelize(card.status_id)}${card.board_id}`);
                let cardToAdd = `
                    <div id="${card.id}" draggable="true" class="${dataHandler.camelize(card.status_id)}" card="true">
                        ${card.title}
                    </div>
                `;
                cardColumn.insertAdjacentHTML('beforeend', cardToAdd);
            }
        }
        this.createDropZone();
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
    createDropZone: function () {
        let dropZone = document.querySelectorAll('.col.border.border-dark.p-0');
        let cards = document.querySelectorAll('div[card="true"]');

        for (let card of cards) {
            card.addEventListener('dragstart', event => {
                event.dataTransfer.setData("text/plain", card.id);
            });
        };
        dom.setUpDropZone(dropZone);

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
    // here comes more features
    setUpDropZone: function (dropZone) {
            for (let zone of dropZone) {
                zone.addEventListener('dragover', event => {
                    event.preventDefault();
                })
            };


            for (let zone of dropZone) {
                zone.addEventListener('drop', event => {
                    let zoneStatus = zone.getAttribute('status');
                    let droppedElementId = event.dataTransfer.getData("text/plain");
                    let droppedElement = document.querySelector(`div[id="${droppedElementId}"]`);
                    zone.appendChild(droppedElement);

                    if (zoneStatus == 'new') {
                        droppedElement.setAttribute('class', 'new');
                    } else if (zoneStatus == 'inProgress') {
                        droppedElement.setAttribute('class', 'inProgress');
                    } else if (zoneStatus == 'testing') {
                        droppedElement.setAttribute('class', 'testing');
                    } else if (zoneStatus == 'done') {
                        droppedElement.setAttribute('class', 'done');
                    }

                });
            }
        },
};
