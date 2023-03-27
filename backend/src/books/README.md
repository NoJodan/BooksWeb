# <center>DOCS</center>

### URL: `/api/books`

### POST `/api/books/`
This action creates a new book in the database
> example request
> ```js
> const payload = {
>   book:{
>       name: 'Example name'
>       description: 'Example description'
>       author: 'Example author'
>   }
> }
> const options = {
>  method: 'POST',
>  headers: {
>    'Content-Type': 'application/json',
>    'Authorization': 'Bearer <token>'
>  },
>  body: JSON.stringify(payload)
> };
>
> fetch('http://example.com/api/books', options).then(response => {
>   //Your code here    
>})
>```
> #### example response
> ```json
> {
>   "msg": "Book created",
>   "status": {
>        "name": "created",
>        "action": "create",
>        "create": true
>    }
> }
> ```
> #### error response
> ```json
>  {
>    "msg": "No book provided",
>    "status": {
>        "name": "not_created",
>        "action": "create",
>        "create": false
>    }
>  }
> ```

### GET `/api/books/`
This action returns all books in the database
> ## params
> * poster
> 
>
> ### poster options
> * @me
> * @others 
> * @all
>
> #### @me
> * returns all books published by the requesting user
> #### @others
> * returns all books in the database except those of the requesting user

> #### @all
> * returns all books in the database


> exmaple request
> ```js
>const options = {
>   method: 'GET',
>   headers: {    
>       'Authorization': 'Bearer <token>'
>   }
>};
>fetch('http://example.com/api/books', options).then(response => {
>   //Your code here    
>})
> ```

> #### example response
> ```json
> {
>   "msg": "Books retrieved",
>   "status": {
>        "name": "retrieved",
>        "action": "get",
>        "get": true
>    }
> }
> ```


### GET `/api/books/<id>`
This action returns a book in the database getted by id

> example request
> ```js
>const options = {
>   method: 'GET',
>   headers: {
>       'Authorization': 'Bearer <token>'  
>   }
>};
>
>fetch('http://example.com/api/books/1', options).then(response => {
>   //Your code here    
>})
> ```

> #### example response
> ```json
> {
>   "msg": "Book retrieved",
>   "status": {
>        "name": "retrieved",
>        "action": "get",
>        "get": true
>    }
> }
> ```
> #### error response
> ```json
>  {
>    "msg": "Book not found",
>    "status": {
>        "name": "not_found",
>        "action": "get",
>        "get": false
>    }
>  }
> ```

### DELETE `/api/books/<id>`
This action deletes a book in the database

> example request
> ```js
>const options = {
>    method: 'DELETE'
>    headers: {
>        'Authorization': 'Bearer <token>'
>    }
>};
>
>fetch('http://example.com/api/books/1', options).then(response => {
>   //Your code here    
>})
> ```

> #### example response
> ```json
> {
>   "msg": "Book deleted",
>   "status": {
>        "name": "deleted",
>        "action": "delete",
>        "delete": true
>    }
> }
> ```
> #### error response
> ```json
>  {
>    "msg": "Book not found",
>    "status": {
>        "name": "not_found",
>        "action": "delete",
>        "delete": false
>    }
>  }
> ```

### PUT `/api/books/<id>`
This action updates a book in the database

> example request
> ```js
> const payload = {
>   book:{
>       name: 'Example name'
>       description: 'Example description'
>       author: 'Example author'
>   }
> };
> const options = {
>  method: 'PUT',
>  headers: {
>    'Content-Type': 'application/json',
>    'Authorization': 'Bearer <token>'
>  },
>  body: JSON.stringify(payload)
> };
>
>fetch('http://example.com/api/books/1', options).then(response => {
>   //Your code here    
>})
> ```

> #### example response
> ```json
> {
>   "msg": "Book updated",
>   "status": {
>        "name": "updated",
>        "action": "update",
>        "update": true
>    }
> }
> ```
> #### error response
> ```json
>  {
>    "msg": "Invalid book",
>    "status": {
>        "name": "not_updated",
>        "action": "update",
>        "update": false
>    }
>  }
> ```
