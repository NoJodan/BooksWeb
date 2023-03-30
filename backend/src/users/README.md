# DOCS

### POST `/api/users`
This action is used to register a new user.

> example request with javascript
>
> ```js
> const payload = {
>   username: 'john',
>   password: 'secret'
> }
>
> const options = {
>   method: 'POST',
>   headers: {
>     'Content-Type': 'application/json'
>   },
>   body: JSON.stringify(payload)
> }   
> 
> fetch('http://localhost:8000/api/users', options).then(response => {
>   //Your code here    
>});
> ```

> #### example response
> ```json
> {
>   "msg": "User created successfully",
>   "status": {
>        "name": "created",
>        "action": "register",
>        "register": true
>    }
> }
> ```
> #### error response
> ```json
>  {
>    "msg": "Invalid username",
>    "status": {
>        "name": "invalid_data",
>        "action": "register",
>        "register": false
>    }
>  }
> ```


### GET `/api/users`
This action is used to login a user.

> example request
>
> ```js
> const username = 'john';
> const password = 'secret';
> 
> const payload = btoa(`${username}:${password}`);
>    
> const options = {
>   method: 'GET',
>   headers: {
>       'Authorization': `Basic ${payload}`
>   }
> }
> fetch('http://localhost:8000/api/users', options).then(response => {
>   //Your code here
>});
> ```

> ## params
> * stay_loged_in
>
>
> #### stay_loged_in options
>   * `true`
>   * `false`
>
> #### `true`
> * returns a token that expires in 7 days

> #### `false`
> * returns a token that expires in 24 hours

> #### example response
> ```json
> {
>   "msg": "User logged in successfully",
>   "status": {
>        "name": "logged_in",
>        "action": "login",
>        "login": true
>    },
>   "data":{
>       "token": "<token>" 
>   }
> }
> ```
> #### error response
> ```json
>  {
>    "msg": "Invalid credentials",
>    "status": {
>        "name": "invalid_data",
>        "action": "login",
>        "login": false
>    }
>  }
> ```

### PUT `/api/users`
This action is used to update a user.

> example request with javascript
>
> ```js
> const payload = {
>   user: {
>       username: 'john 2',
>   }
> }
>
> const options = {
>   method: 'PUT',
>   headers: {
>     'Content-Type': 'application/json'
>   },
>   body: JSON.stringify(payload)
> }   
> 
> fetch('http://localhost:8000/api/users', options).then(response => {
>   //Your code here    
>});
> ```

> #### example response
> ```json
> {
>   "msg": "User update successfully",
>   "status": {
>        "name": "update",
>        "action": "update",
>        "update": true
>    }
> }
> ```
> #### error response
> ```json
>  {
>    "msg": "Invalid user",
>    "status": {
>        "name": "not_updated",
>        "action": "update",
>        "update": false
>    }
>  }
> ```