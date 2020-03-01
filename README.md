# Surveys API

This is an APi that can be used to store surveys and user responses to said
surveys.

<!-- vim-markdown-toc GFM -->

* [Prerequisites](#prerequisites)
* [Run the app](#run-the-app)
* [API Documentation](#api-documentation)

<!-- vim-markdown-toc -->

## Prerequisites

* [Python v3](https://www.python.org/)
* [PostgreSQL v10+](https://www.postgresql.org/)
* [pip-tools](https://pypi.org/project/pip-tools/)
  * This is used to install dependencies listed in the
    [`.requirements.txt` file](https://github.com/kohrVid/surveys_api/blob/master/requirements.txt)


## Run the app

This is a [django](https://www.djangoproject.com/) application so the typical
`python manage.py` can be used to run the webserver and migrations, &c. I have
added a Makefile for simplicity so `make` commands can be used to install and
run the application instead.

To install dependencies, create the PostgreSQL database and run migrations:

    make install

To only create the database:

    make db-create

To only run migrations:

    make db-migrate

To truncate all rows in the database:

    make db-clean

To drop the database:

    make db-drop

To run the webserver:

    make serve

To run the test suite:

    make test

To run tests with inotify:

    make test-hot-reload


## API Documentation

This application comes with swagger documentation for the API. When the server
is run on `localhost:8000`, the Swagger UI can be viewed
[here](http://localhost:8000/swagger-ui) and the JSON version of the API
documentation can be found [here](http://localhost:8000/swagger.json).
