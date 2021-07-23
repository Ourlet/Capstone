# Capstone Project - Nano Degree FullStack Developer

## Usefull links

Heroku link : https://capstone-ourlet.herokuapp.com/ 
Run locally on : http://127.0.0.1:5000/

## Getting Started

### Dependencies

In order to launch the project, the developer should have installed:

* Python 3.7
* pip 3
* Flask
* SQLAlchemy

As well as all the requirements for this project by running:

```bash
pip install -r requirements.txt
```
### Running the server

To run the server, execute:
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the FLASK_ENV variable to development will detect file changes and restart the server automatically.

## API Reference
### Roles
The application has three type of roles:
- Casting Assistant
    - Can view actors and movies
    - has get:actors, get:movies permissions

- Casting Director
    - All permissions a Casting Assistant has and Add or delete an actor from the database and Modify actors or movies
    - has get:actors, get:movies, delete:actor,patch:actor, patch:movie, post:actor	permissions

- Executive Producer
    - All permissions a Casting Assistant has and Add or delete a movie from the database
    - has delete:movie, get:actors, get:movies, post:movie permissions

### Error Handling
Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return four error types when requests fail:
* 400: Bad Request
* 401: Unauthorized
* 403: Forbidden
* 404: Resource Not Found
* 422: Not Processable
* 500: Internal Server Error

### Endpoints
### GET /movies
* Return the list of all movies
* Requires get:movies permission
* Sample request : https://capstone-ourlet.herokuapp.com/movies

```
{
  "movies": [
    {
      "distribution": [], 
      "id": 1, 
      "title": "Terminator"
    }, 
    {
      "distribution": [], 
      "id": 2, 
      "title": "The expendables 2"
    }, 
    {
      "distribution": [], 
      "id": 3, 
      "title": "Predator"
    }
  ], 
  "success": true
}
```

### GET /actors
* Return the list of all actors
* Requires get:actors permission
* Sample request : https://capstone-ourlet.herokuapp.com/actors

```
{
  "actors": [
    {
      "age": 75, 
      "gender": "M", 
      "id": 3, 
      "name": "Sylverster Stalone"
    }, 
    {
      "age": 38, 
      "gender": "F", 
      "id": 4, 
      "name": "Giselle Itie"
    }, 
    {
      "age": 88, 
      "gender": "M", 
      "id": 6, 
      "name": "Gerard Depardieu"
    }, 
}
```

### POST /movies
* Create a new movie
* Requires post:movie
* Request Body:
    - title: String, required
    - release_date: datetype, required
* Sample Request - https://capstone-ourlet.herokuapp.com/movies
* Sample Body
```
{
    "title": "Jurassic Park", 
    "release_date": "2018-01-11"
}
```

### POST /actors
* Create a new actor
* Requires post:actor
* Request Body:
    - name: String, required
    - gender: String, required
    - age: Integer, required
* Sample Request - https://capstone-ourlet.herokuapp.com/actors
* Sample Body
```
{
    "name": "Gerard Depardieu", 
    "gender": "M", 
    "age": 78
}
```
### PATCH /movies/id
* Update data of a movie
* Requires patch:movie permission
* Request body (at least one of the following);
    - title: String, required
    - release_date: datetype, required
* Sample Request - https://capstone-ourlet.herokuapp.com/movies/1
* Sample Body 
```
{
    "title": "Le grand Bleu"
}
```
### PATCH /actors/id
* Update data of an actor
* Requires patch:actor permission
* Request body (at least one of the following);
    - name: String, required
    - gender: String, required
    - age: Integer, required
* Sample Request - https://capstone-ourlet.herokuapp.com/actors/3
* Sample Body 
```
{
    "name": "Jean Reno"
}
```
### DELETE /movies/id
* Delete a movie
* Requires delete:movie permission
* Sample request - https://capstone-ourlet.herokuapp.com/movies/1

### DELETE /actors/id
* Delete an actor
* Requires delete:actor permission
* Sample request - https://capstone-ourlet.herokuapp.com/actors/1

