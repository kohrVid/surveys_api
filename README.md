# Surveys API

This is an API that can be used to store surveys and user responses to said
surveys.

<!-- vim-markdown-toc GFM -->

* [Prerequisites](#prerequisites)
* [Using the application](#using-the-application)
  * [Install](#install)
  * [Run the app](#run-the-app)
  * [Drop the database](#drop-the-database)
  * [Typical usage](#typical-usage)
* [API Documentation](#api-documentation)

<!-- vim-markdown-toc -->

## Prerequisites

* [Python v3](https://www.python.org/)
* [PostgreSQL v10+](https://www.postgresql.org/)
* [pip-tools](https://pypi.org/project/pip-tools/)
  * This is used to install dependencies listed in the
    [`.requirements.txt` file](https://github.com/kohrVid/surveys_api/blob/master/requirements.txt)
* The [`.env` file](https://github.com/kohrVid/surveys_api/blob/master/.env) in the root of this repo
  (it contains important configuration for the application)


## Using the application

This is a [django](https://www.djangoproject.com/) application so the typical
`python manage.py` can be used to run the webserver and migrations, &c. I have
added a Makefile for simplicity so `make` commands can be used to install and
run the application instead.


### Install

To install dependencies, create the PostgreSQL database and run migrations:

    make install

To only create the database:

    make db-create

To only run migrations:

    make db-migrate


### Run the app

To run the webserver:

    make serve

The app can be viewed on [http://localhost:8000](http://localhost:8000).

To run the test suite:

    make test

To run tests with [inotify](https://en.wikipedia.org/wiki/Inotify):

    make test-hot-reload


### Drop the database

To truncate all rows in the database:

    make db-clean

To drop the database:

    make db-drop


### Typical usage

When using this application for the first time, it usually makes sense to create
a user account. An admin user can be created with the following command:

    python manage.py createsuperuser

It is however possible to create a user with a cURL request as well:

    curl 'http://localhost:8000/users' \
    --header 'Content-Type: application/json' \
    --data-raw '{
            "username": "artemis",
            "email": "artemis.bishop@axample.com"
        }'

New surveys for the user can be created by posting to either `/surveys` or
`/users/:user_id/surveys`. Both endpoints require the same parameters for now
(though I would prefer if the `user_id` field could be dropped from the request
body in the latter):

    curl 'http://localhost:8000/surveys/' \
      --header 'Content-Type: application/json' \
      --data-raw '{
              "name": "Opinions about apples",
              "available_places": 30,
              "user_id": 1
      }'


or

    curl 'http://localhost:8000/users/1/surveys/' \
      --header 'Content-Type: application/json' \
      --data-raw '{
              "name": "Opinions about apples",
              "available_places": 30,
              "user_id": 1
      }'

(Note the redundant `user_id` field in the body of the second request.)

The surveys created for a particular user can be seen by making a GET request
to `/users/:user_id/surveys`:

    curl --location --request GET 'http://localhost:8000/users/1/surveys' \
      --header 'Content-Type: application/json'


New survey responses can be created with a POST request to `/survey-responses` or
`/users/:user_id/survey-responses`:

    curl --location --request POST 'http://localhost:8000/survey-responses' \
      --header 'Content-Type: application/json' \
      --data-raw '{
              "survey_id": 1,
              "user_id": 1
      }'

or,

    curl --location --request POST 'http://localhost:8000/users/1/survey-responses' \
      --header 'Content-Type: application/json' \
      --data-raw '{
              "survey_id": 1,
              "user_id": 1
      }'

Note that both of the fields in the survey response refer to other tables
(`surveys_survey` and `auth_user`). In the future, it would probably make sense
to add a text field to the `surveys_surveyresponse` table so that user responses
to a given survey are recorded as well. At present it functions similarly to an
[associative table](https://en.wikipedia.org/wiki/Associative_entity) between
the Survey and the User models.

It should be possible to list all of the survey responses for a given user...

    curl --location --request GET 'http://localhost:8000/users/1/survey-responses' \
      --header 'Content-Type: application/json'


...as well as the responses given to a particular survey...

    curl --location --request GET 'http://localhost:8000/surveys/1/survey-responses' \
      --header 'Content-Type: application/json'




## API Documentation

This application comes with swagger documentation for the API. When the server
is run, the Swagger UI can be viewed [here](http://localhost:8000/swagger-ui)
and the JSON version of the API documentation can be found
[here](http://localhost:8000/swagger.json).
