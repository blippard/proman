// this object contains the functions which handle the data and its reading/writing
// feel free to extend and change to fit your needs

// (watch out: when you would like to use a property/function of an object from the
// object itself then you must use the 'this' keyword before. For example: 'this._data' below)
export let dataHandler = {
  _data: {}, // it is a "cache for all data received: boards, cards and statuses. It is not accessed from outside.
  _api_get: function (url, callback) {
    // it is not called from outside
    // loads data from API, parses it and calls the callback with it

        fetch(url, {
            method: 'GET',
            credentials: 'same-origin'
        })
        .then(response => response.json())  // parse the response as JSON
        .then(json_response => callback(json_response));  // Call the `callback` with the returned object
    },
    _api_post: function (url, data, callback) {
    // it is not called from outside
    // sends the data to the API, and calls callback function
    fetch(url, {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    })
      .then((response) => response.json()) // parse the response as JSON
      .then((json_response) => callback(json_response)); // Call the `callback` with the returned object
  },
    _api_put: function (url, data, callback) {
        fetch(url, {
            method: 'PUT',
            body: JSON.stringify(data),
            headers: new Headers({
                "content-type": "application/json"
            })
        }).then(function (response) {
            if (response.status !== 200) {
                console.log(`Looks like there was a problem. Status code: ${response.status}`);
                return;
            }
        }).then(callback)
    },
    init: function () {
    },
    getBoards: function (callback) {
        // the boards are retrieved and then the callback function is called with the boards

        // Here we use an arrow function to keep the value of 'this' on dataHandler.
        //    if we would use function(){...} here, the value of 'this' would change.
        this._api_get('/get-boards', (response) => {
            this._data['boards'] = response;
            callback(response);
        });
    },
    getBoard: function (boardId, callback) {
        // the board is retrieved and then the callback function is called with the board
    },
    getBoardStatuses: function (boardId, callback) {
        // the statuses are retrieved and then the callback function is called with the statuses
        this._api_get(`/get-board-statuses/${boardId}`, (response) => {
            callback(response);
        })
    },
    getStatus: function (statusId, callback) {
        // the status is retrieved and then the callback function is called with the status
    },
    getCardsByBoardId: function (boardId, callback) {
        // the cards are retrieved and then the callback function is called with the cards
        this._api_get(`/get-cards/${boardId}`, (response) => {
            this._data['cards'] = response;
            callback(response);
        })
    },
    getLatestCardsByBoardId: function (boardId, callback) {
        // the cards are retrieved and then the callback function is called with the cards
        this._api_get(`/get-cards/${boardId}`, (response) => {
            this._data['cards'] = response;
            callback(response[response.length - 1]);
        })
    },
    getCard: function (cardId, callback) {
        // the card is retrieved and then the callback function is called with the card
    },
    createNewBoard: function (boardTitle, callback) {
        // creates new board, makes a request to save it and calls the callback function with its data
        let dataToPost = { title: boardTitle };
        this._api_post("/add-board", dataToPost, (jsonResponse) => {
          if (jsonResponse.title) {
            this._data["boards"].push(jsonResponse);
          }
          callback(jsonResponse);
        }); //callback will act on response.json(),
            // not on response
      },
    createNewCard: function (cardTitle, boardId, statusId, callback) {
        // creates new card, saves it and calls the callback function with its data
        let newCardPostData = {'title': cardTitle, 'board_id': boardId, 'status_id':statusId}
        this._api_post('/add-card', newCardPostData, (jsonResponse) => {
        this._data["cards"].push(jsonResponse);
        })
    },
    renameBoard: function (boardId, title, callback) {
        let newNameBoard = {'board_id': boardId, 'title': title};
        this._api_post('/rename-board', newNameBoard, (jsonResponse) => {
            this._data["boards"].push(jsonResponse);
        })
    },
    renameColumn: function (oldName, title, callback) {
        let newNameColumn = {'old-name': oldName, 'title': title};
        this._api_post('/rename-column', newNameColumn, (jsonResponse) => {
            this._data["statuses"].push(jsonResponse);
        })
    },
    // NOT YET
    // renameCard: function (cardId, title, callback) {
    //     let newNameColumn = {'card-id': cardId, 'title': title};
    //     this._api_post('/rename-column', newNameCard, (jsonResponse) => {
    //         this._data["statuses"].push(jsonResponse);
    //     })
    // },
    // here comes more features
    camelize: function (str) {
    return str.replace(/(?:^\w|[A-Z]|\b\w)/g, function(word, index) {
        return index === 0 ? word.toLowerCase() : word.toUpperCase();
    }).replace(/\s+/g, '');
    },
    deleteBoard: function (boardId, callback) {

    },
};
