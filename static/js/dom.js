// It uses data_handler.js to visualize elements
import {dataHandler} from "./data_handler.js";

export let dom = {
    init: function () {
        let homeButton = document.getElementById('home');
        let registrationButton = document.getElementById('registration-button');
        let registerSubmit = document.getElementById('reg-button');
        let loginButton = document.getElementById('login-button');
        let loginSubmit = document.getElementById('login-submit-button');
        let boards = document.getElementById('boards');
        let registrationContainer = document.getElementById('registration-container');
        let loginContainer = document.getElementById('login-container');
        homeButton.addEventListener('click', () => {
            registrationContainer.style.display = 'none';
            loginContainer.style.display = 'none';
            boards.style.display = 'block';
        })
        registrationButton.addEventListener('click', () => {
            registrationContainer.style.display = 'flex';
            boards.style.display = 'none';
        });
        loginButton.addEventListener('click', () => {
            loginContainer.style.display = 'flex';
            boards.style.display = 'none';
        });
        registerSubmit.addEventListener('click', () => {
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
                    boards.style.display = 'block';
                }
            })
        });
        loginSubmit.addEventListener('click', () => {
            let username = document.getElementById('login-username');
            let password = document.getElementById('login-password');
            this.postdata('http://127.0.0.1:5000/login', {
                username: username.value,
                password: password.value
            }).then((response) => {
                if (response === 'Failure') {
                    alert('Invalid username or password!')
                } else {
                    sessionStorage.setItem("userId", response);
                    loginContainer.style.display = 'none';
                    boards.style.display = 'block';
                }
            })
        })
        // This function should run once, when the page is loaded.
        this.initModalSubmit();
        const newBoardBtn = document.querySelector(".add-board-btn");
        newBoardBtn.addEventListener("click", (event) => {
            this.handleAddBoardClick(event);
        });
    },
    postdata: async function (url = '', data) {
        const response = await fetch(url, {
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

    let boardList = "";

        for(let board of boards){
            let columnlist = '';
            for (let column of board.board_statuses){
                columnlist += `
                <div class="col border border-dark p-0 ${dataHandler.camelize(column)}${board.id}">
                    <div class="card-column-title text-center border-bottom border-dark mb-2">${column}</div>
                </div>
                `
            }
            boardList += `
                <section class="board col mb-5 border border-dark" id="wholeBoard${board.id}">
                    <div class="board-header">
                        <span class="board-title">${board.title}</span>
                        <button class="mc-button add-column" data-toggle="modal" data-target="#submitModal" data-board-id="${board.id}" data-submit-action="addColumn">Add column</button>
                        <button class="btn btn-dark mt-2 float-right" type="button" data-toggle="collapse" data-target="#board${board.id}" aria-expanded="false" aria-controls="board${board.id}">
                            &#x2304
                        </button>
                        <button class="new-card-btn" board-id="${board.id}">New Card</button>
                        <button class="rename-board-btn" board-id="${board.id}" board-title="${board.title}">
                          Rename Board
                        </button>
                        <button class="remove-board-btn">Delete Board &#x1F5D1</button>                       
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

        this.addCardEventListener();
        document.querySelectorAll(".remove-board-btn").forEach((item) => {
          item.addEventListener("click", (event) => {
            // the .board is the grandparent of the .remove-board-btn (the parent is .board-header)
            this.handleRemoveBoardClick(item.parentNode.parentNode, event);
          });
        });
        this.newNameBoardEventListener();
        this.initColumnTitleRename();
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

    newNameBoardEventListener: function () {
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
        dataHandler.getCardsByBoardId(boardId, function (cards) {
            dom.showCards(cards);
        })
    },
    loadLatestCards: function (boardId) {
        // retrieves cards and makes showCards called
        dataHandler.getLatestCardsByBoardId(boardId, function (cards) {
            dom.showCard(cards);
        })
    },

    showCards: function (cards) {
        // shows the cards of a board
        // it adds necessary event listeners also
        for (let card of cards) {
            let board = document.querySelector(`#board${card.board_id}`);
            if (`board${card.board_id}` == `${board.id}`) {
                let cardColumn = board.querySelector(`.${dataHandler.camelize(card.status_id)}${card.board_id}`);
                let cardToAdd = `
                    <div id="${card.id}" draggable="true" class="card mx-0 mb-2 border border-dark text-center ${dataHandler.camelize(card.status_id)}" card="true">
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
    createNewChildBoard: function (board) {
        const boardInnerContainer = document.querySelector(".board-container");
        let columnlist = '';
            for (let column of board.board_statuses){
                columnlist += `
                <div class="col border border-dark p-0 ${dataHandler.camelize(column)}${board.id}">
                    <div class="card-column-title text-center border-bottom border-dark mb-2">${column}</div>
                </div>
                `
            }
        let childHTMLText = `
            <section class="board col mb-5 border border-dark" id="wholeBoard${board.id}">
                <div class="board-header">
                    <span class="board-title">${board.title}</span>
                    <button class="mc-button add-column" data-toggle="modal" data-target="#submitModal" data-board-id="${board.id}" data-submit-action="addColumn">Add column</button>
                    <button class="btn btn-dark mt-2 float-right" type="button" data-toggle="collapse" data-target="#board${board.id}" aria-expanded="false" aria-controls="board${board.id}">
                        &#x2304
                    </button>
                    <button class="new-card-btn" board-id="${board.id}">New Card</button>
                    <button class="rename-board-btn" board-id="${board.id}" board-title="${board.title}">
                        Rename Board
                    </button>
                    <button class="remove-board-btn">Delete Board &#x1F5D1</button>

                </div>
                <div class="row collapse" id="board${board.id}">
                    ${columnlist}
                </div>
            </section>
                `;
        boardInnerContainer.insertAdjacentHTML("beforeend", childHTMLText);
        let newRenameBoardBtn = boardInnerContainer.lastElementChild.querySelector(
            ".rename-board-btn"
        );
        newRenameBoardBtn.addEventListener("click", (event) => {
            event.preventDefault();
            this.handleRenameBoardClick(newRenameBoardBtn);
        });

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
        let boardId = parseInt(boardNode.id.substring(9)) // remove the first 10 chars of id=
        dataHandler.deleteBoard(boardId, (jsonResponse) => {
        if (!(jsonResponse.id)) {
            window.alert(
            "Could not get reply from server. Will delete only temporarily!"
            );
        }
        });
        // window.alert(`Deleted board with id=${boardNode.dataset.id}`)
        boardNode.remove(); // this will remove all children of the node as well
    },
    handleRenameBoardClick: function (boardBtnElement) {
        let boardTitle = boardBtnElement.parentNode.querySelector(".board-title").innerText;
        let boardId = boardBtnElement.parentNode.parentNode.dataset.id;
        let cardForm = `
        <form>
            <input type="text" name="title" placeholder="${boardTitle}" value="${boardTitle}">
            <input type="submit" id="new-board-name-submit" value="Save">
        </form>
        `
        boardBtnElement.insertAdjacentHTML("afterend", cardForm);
        let form = document.querySelector('form')
            form.addEventListener('submit', event => {
                const formData = new FormData(event.target)
                dataHandler.renameBoard(boardId, formData.get('title'));
            })
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
    
    // here comes more features
    removeAllBoardElements: function () {
        let allBoards = document.querySelector('#boards');
        if (allBoards) {
            allBoards.innerHTML = '';
        }
    },
    initAddColumn: function (event) {
        let boardSection = event.target.parentNode.parentNode;
        if (boardSection.tagName === 'SECTION' && boardSection.classList.contains('board')) {
            document.querySelector('#submitModalTitle').innerText = 'Add new column';
            document.querySelector('#submitModalInputPrepend').innerText = 'Column name:';
            document.querySelector('#submitModalInput').value = '';
            let submitModal = document.querySelector('#submitModal');
            submitModal.dataset.boardId = event.target.dataset.boardId;
            submitModal.dataset.submitAction = event.target.dataset.submitAction;
        }
    },
    initModalSubmit: function () {
        document.querySelector('#modalSubmitButton').addEventListener('click', () => {
            let submitModal = document.querySelector('#submitModal')
            if (submitModal.querySelector('#submitModalInput').value) {
                if (submitModal.dataset.submitAction === "addColumn") {
                    let boardId = submitModal.dataset.boardId;
                    let columnTitle = submitModal.querySelector('#submitModalInput').value;
                    dataHandler.createNewColumn(columnTitle, boardId, (data) => {
                        this.addNewColumn(boardId, data.columnTitle);
                    });
                }
            }
        })
    },
    addNewColumn: function (boardId, columnTitle) {
        let board = document.querySelector(`#board${boardId}`);
        let newColumn = `
        <div class="col border border-dark p-0 ${dataHandler.camelize(columnTitle)}${boardId}">
            <div class="'card-column-title text-center border-bottom border-dark mb-2'">${columnTitle}</div>
        </div>
        `
        board.insertAdjacentHTML('beforeend', newColumn);
    },
    initColumnTitleRename: function () {
        let columnTitles = document.querySelectorAll('.card-column-title');
            for (let colTitle of columnTitles) {
                colTitle.addEventListener("click", function () {
                    let oldName = `${colTitle.innerText}`;
                    let columnTitle = `${colTitle.innerText}`;
                    let addName = `
                        <form>
                        <input type="text" name="title" placeholder="${columnTitle}" value="${columnTitle}">
                        <input type="submit" id="new-board-name-submit" value="Save">
                        </form>
                        `
                    colTitle.insertAdjacentHTML("afterend", addName);
                    let form = document.querySelector('form')
                    form.addEventListener('submit', event => {
                        const formData = new FormData(event.target)
                        dataHandler.renameColumn(oldName, formData.get('title'));
                    })
                });
            }
    },
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
                        let postData = {'id': droppedElementId, 'status': '0'};
                        // console.log(postData);
                        dataHandler._api_post('/update-card', postData, (jsonResponse) => {
                        dataHandler._data["cards"].push(jsonResponse);
                        })
                    } else if (zoneStatus == 'inProgress') {
                        droppedElement.setAttribute('class', 'inProgress');
                        let postData = {'id': droppedElementId, 'status': '1'};
                        // console.log(postData);
                        dataHandler._api_post('/update-card', postData, (jsonResponse) => {
                        dataHandler._data["cards"].push(jsonResponse);
                        })
                    } else if (zoneStatus == 'testing') {
                        droppedElement.setAttribute('class', 'testing');
                        let postData = {'id': droppedElementId, 'status': '2'};
                        // console.log(postData);
                        dataHandler._api_post('/update-card', postData, (jsonResponse) => {
                        dataHandler._data["cards"].push(jsonResponse);
                        })
                    } else if (zoneStatus == 'done') {
                        droppedElement.setAttribute('class', 'done');
                        let postData = {'id': droppedElementId, 'status': '3'};
                        // console.log(postData);
                        dataHandler._api_post('/update-card', postData, (jsonResponse) => {
                        dataHandler._data["cards"].push(jsonResponse);
                        })
                    }
              });
          }
      },
};
