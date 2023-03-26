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
> fetch('http://example.com/api/books', options)
>
>```
>
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
>
> #### @me
> * returns all books published by the requesting user
> #### @others
> * returns all books in the database except those of the requesting user


> exmaple request
> ```js
>const options = {
>   method: 'GET',
>   headers: {    
>       'Authorization': 'Bearer <token>'
>  };
>
>fetch('http://example.com/api/books', options).then(response => response.json())
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
>fetch('http://example.com/api/books/1', options).then(response => response.json())
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
>fetch('http://example.com/api/books/1', options).then(response => response.json())
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
>fetch('http://example.com/api/books/1', options).then(response => response.json())
> ```