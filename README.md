# JellySmackTest

This is my technical test for Jellysmack. Made in Python 3.8 with FastAPI and SQLAlchemy.


# Installation
Pre-requisites: Have Python 3.8 and pip installed
```bash
# Install virtualenv
pip install -U virtualenv
# Create a new virtual environment ("venv")
virtualenv venv
# Activate the venv
source venv/bin/activate
# Install all the project dependencies
pip install -r requirements.txt
```

# Commands
The commands are made easier to run with a Makefile. If you want to run them yourself check out the Makefile.

#### Install Dependencies
```bash
make setup
```

#### Import Episodes and Comments from data folder

```bash
# This is also useful for resetting the database.
# Use make import_data_keep_tables to not delete previous Episodes, Characters and Appearances
# Use make import_data_drop_tables to also delete Comments and Users
make import_data
```
#### Launch the API (available at http://127.0.0.1:8000/)
```bash
make run
```

#### Lint Code (flake8)
```bash
make lint
```

#### Run Tests
```bash
make tests
```

#### Run Test Coverage
```bash
make coverage
```

# API Routes
*All the accessible routes and their parameters can be found at http://127.0.0.1:8000/docs*

Available routes are as follow:

| Method | Route | Description |
| ------ | ------ | ------ |
| [GET] | /api/v1/episodes | List and Filter Episodes |
| [GET] | /api/v1/characters | List and Filter Characters |
| [GET] | /api/v1/comments |  List and Filter Comments |
| [POST] | /api/v1/comments |  Create a Comment |
| [PUT] | /api/v1/comment/{id} | Update a Comment |
| [DELETE] | /api/v1/comment/{id} | Delete a Comment |
| [GET] | /api/v1/comments/export_csv | Export Comments as CSV file |
| [GET] | /api/v1/users | List and Filter Users |
| [GET] | /api/v1/users/me | Get Authenticated User's Info |
| [POST] | /api/v1/signup | Create a User |
| [PUT] | /api/v1/users | Update a User |
| [PUT] | /api/v1/users/me | Update Authenticated User's Info |
| [DELETE] | /api/v1/users | Delete a User |
| [DELETE] | /api/v1/users | Delete Authenticated User |
| [GET] | /api/v1/users/me/comments | List and Filter Authenticated User's Comments |
| [POST] | /api/v1/token | Authenticate with username and password and get a JWT token |
| [GET] | / | Home |

