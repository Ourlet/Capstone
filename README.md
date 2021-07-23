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
}```

The API will return four error types when requests fail:
* 400: Bad Request
* 401: Unauthorized
* 403: Forbidden
* 404: Resource Not Found
* 422: Not Processable
* 500: Internal Server Error

### Endpoints
###GET /movies