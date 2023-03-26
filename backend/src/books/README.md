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
>  headers: {'Content-Type': 'application/json'},
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

### GET `api/books/`

> exmaple request
> ```js
>const options = {method: 'GET'};
>
>fetch('http://example.com/api/books', options).then(response => response.json())
> ```