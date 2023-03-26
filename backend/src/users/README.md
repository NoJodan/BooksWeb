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
