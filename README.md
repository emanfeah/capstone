# FSND_Capstone_Casting_Agency
Fullstack Nanodegree Final Project - Casting Agency

# Casting Agency
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

No frontend developed yet, only server side.

Application hosted on Heroku 

https://vast-stream-21858.herokuapp.com/

# Motivation

This project to show my learning journey during this nanodegree

1.  Database with  **postgres**  and  **sqlalchemy**  (`models.py`)
2.  API  with  **Flask**  (`app.py`)
3.  TDD  **Unittest**  (`test_app.py`)
4.  Authorization &  Authentification **Auth0**  (`auth.py`)
5.  Deployment on  **`Heroku`**

## Working with the application locally
Make sure you have [python 3](https://www.python.org/downloads/) or later installed

1. **Clone The Repo**
    ```bash
    git clone https://github.com/emanfeah/capstone.git
    ```
2. **Set up a virtual environment**:
    ```bash
    virtualenv env
    source env/Scripts/activate # for Windows
    source env/bin/activate # for MacOs/Linux
    ```
3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt # for Windows/Linux
    pip3 install -r requirements.txt # for MacOs
    ```
4. **Export Environment Variables**

    Refer to the `setup.sh` file and export the environment variables for the project.

5. **Create Local Database**:

    Create a local database and export the database URI as an environment variable with the key `DATABASE_URL`.

6. **Run Database Migrations**:
    ```bash
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    ```

7. **Run the Flask Application locally**:
    ```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development
    flask run

    # if using CMD in Windows

    set FLASK_APP=app.py
    set FLASK_ENV=development
    flask run
    ```

## Testing
To run the tests, run
```bash
dropdb capstone
createdb capstone
python test_app.py # if running locally
```

## API Reference

### Getting Started

* Base URL: Currently this application is only hosted locally. The backend is hosted at `https://glacial-falls-65708.herokuapp.com`
* Authentication: This application use Auth0 service

* Use this link to get new token [Get Token](https://fsnd-udacity.eu.auth0.com/authorize?audience=CastingAgency&response_type=token&client_id=WMvUqnD1GAJg2OH06i4Musq0vllhysMh&redirect_uri=https://localhost:8080/login-results)

Users in this application are:

* Assistant : Can view actors and movies
    * Email: eman21@gmail.com
    * Password: eman21@gmail.com
* Director : Assistant Access + CURD on actors + Modify movies
    * Email: casting_director@gmail.com
    * Password: test12345@pass
* Executive: Full Access
    * Email:executive_producer@gmail.com
    * Password: test12345@pass

### Error Handling

Errors are returned as JSON in the following format:<br>

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

The API will return three types of errors:

* 404 – resource not found
* 422 – unprocessable
* 401 - Unauthorized
* 400 - bad request
* 500 - internal server error
* 405 - method not allowed

### Endpoints

#### GET /actors


* General: Return list of actors in Database
* Sample: `curl -L -X GET 'glacial-falls-65708.herokuapp.com/actors' \
-H 'Authorization: Bearer Assisant_Token'`<br>

        {
            "actors": [
                {
                    "age": 20,
                    "gender": "fmale",
                    "id": 1,
                    "name": "eman"
                }
            ],
            "success": true
        }

#### GET /movies

* General: Return list of movies in Database
* Sample: `curl -L -X GET 'glacial-falls-65708.herokuapp.com/movies' \
-H 'Authorization: Bearer Assisant_Token'`<br>
{
    "movies": [
        {
            "id": 1,
            "release_date": "Sun, 20 Dec 2020 00:00:00 GMT",
            "title": "prada"
        }
    ],
    "success": true
}

#### POST /actors

* General:
    * Create actor using JSON Request Body
    * Return ID of created actor
* Sample: `curl -X POST 'glacial-falls-65708.herokuapp.com/actors' \
-H 'Authorization: Bearer Director_Token' \
-H 'Content-Type: application/json' \
--data-raw '{
    "name":"eman",
    "age":30,
    "gender":"fmale"
}'`
{
    "actors": {
        "age": "30",
        "gender": "fmale",
        "id": 3,
        "name": "eman"
    },
    "success": true
}

#### POST /movies

* General:
    * Create movie using JSON Request Body
    * Return ID of created movie
* Sample: `curl -X POST 'glacial-falls-65708.herokuapp.com/movies' \
-H 'Authorization: Bearer Executive_Token' \
-H 'Content-Type: application/json' \
--data-raw '{
    "title":"prada",
    "release_date" : "December 20, 2020"
}'`

         {
    
            "title": "prada",
            "release_date": "December 20, 2020"

        }

#### PATCH /actors/<actor_id>

* General:
    * Modify actor given id in URL provided the information to update
* Sample: `curl -X PATCH 'glacial-falls-65708.herokuapp.com/actors/3' \
-H 'Authorization: Bearer Director_Token' \
-H 'Content-Type: application/json' \
--data-raw '{
    "name" : "eman",
    "age" : 25
}'`

        {

            "name": "eman",
            "age": 25,
            "gender": "fmale"

        }
#### PATCH /movies/<movie_id>

* General:
    * Modify movie given id in URL provided the information to update
* Sample: `curl -X PATCH 'glacial-falls-65708.herokuapp.com/movies/2' \
-H 'Authorization: Bearer Director_Token' \
-H 'Content-Type: application/json' \
--data-raw '{
    "title":"klous",
    "release_date":"December 20, 2020"
}'`

#### DELETE /actors/<actor_id>

* General: Delete an actor given id in URL
* Sample: `curl -X DELETE 'glacial-falls-65708.herokuapp.com/actors/3' \
-H 'Authorization: Bearer Executive_Token'`

        {
            "deleted_id": 3,
            "success": true
        }

#### DELETE /movies/<movie_id>

* General: Delete movie given id in URL
* Sample: `curl -X DELETE 'glacial-falls-65708.herokuapp.com/movies/2' \
-H 'Authorization: Bearer Executive_Token'`

        {
            "deleted_id": 2,
            "success": true
        }

# Postman user
in this repo there is collection file exported with latest postman version

you can use it to test all API Provided in here

PS: Update Tokens For Folders in the collection