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


# Notes
### Time taken
This project took me about 12 hours (very rough estimate). 

### Thoughts
The part that took me the longest was by far the users and authentication. I chose to go with JWT and OAuth2 because it seemed like the most solid Authentication/Authorization method for FastAPI. In retrospect, that was probably not the right choice for this particular exercise. I realized only too late that I had to implement logging out as wel. And logging out is not a thing with JWT tokens. I could have implemented a token black list stored on Redis, and make a middleware used by every method that needs authentication, to verify that the token is still valid. But for simplicity, that would have involved changing the jwt implementation I chose (python-jose), and a few other things. I decided I was already too far into it.

### Features done and choices made
For the mandatory parts I did everything asked and a little more. I added more complex filters, like the possibility to search characters by episodes they appeared in, and vice versa. Also there is the possibility to search episodes by season number or air date. I decided to make the creation of comments dependant on authentication, even though other methods like update and delete are not. I obviously would not have done that in a real-world situation but it seemed intuitive to tie comment creation to authentication. I also decided to implement routes tied to the authenticated user, like see your own comments, modify your account (update own user), and delete your account.

The project's coverage is 93%

### Possible improvements
If this was an already existing production environment, I would have used Alambic for migrations. As said before, I could have chosen another authentication method for logging out more easily. The next step would have been to add roles and permissions (part of the backlog). The CSV export function is not fully optimized, I would surely use other methods for a very large number of comments. I also could have commented more thoroughly but I feel like the functions I did not comment are pretty self-explanatory.

### Conclusion
It was really interesting to try FastAPI and to work with SQLAlchemy again. I think this test is well made. It's not overly complex for no reason, it's not too long if you don't want to and it's still complete enough to gauge someone's proficiency in buiding APIs and backends in Python. I feel confortable with my level, and even though I could have done more, I feel like I did a good job for the time I took.

