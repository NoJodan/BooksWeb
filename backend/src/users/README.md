# DOCS

### POST `/api/users/register`
This action is used to register a new user.

> example request with javascript
>
> ```js
> const payload = {
>   username: 'john'
>   password: 'secret'
> }
>
> const options = {
>   method: 'POST',
>   headers: {
>     'Content-Type': 'application/json',
>     'Authorization': 'Bearer <token>'
>   },
>   body: JSON.stringify(payload)
> }   
> 
> fetch('http://localhost:8000/api/users/register', options).then(response => {
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


### GET `/api/users/login`
This action is used to login a user.

> example request
>
> ```js
> const username = 'john':
> const password = 'secret';
> 
> const payload = btoa(`${username}:${password}`);
>    
> const options = {
>   method: 'POST',
>   headers: {
>       'Authorization': `Basic ${payload}`
>   }
> }
> fetch('http://localhost:8000/api/users/login', options).then(response => {
>   //Your code here
>});
> ```

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
