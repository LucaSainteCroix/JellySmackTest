from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
import pytest

import main
from database.database import Base, get_db
from models.models import Character, Episode, Appearance, Comment, User, StatusEnum, GenderEnum

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    Episode.__table__.drop(engine)
    Character.__table__.drop(engine)
    Appearance.__table__.drop(engine)
    Comment.__table__.drop(engine)
    User.__table__.drop(engine)
except OperationalError:
    # If we get here it is probably because tables don't exists
    pass


Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

main.app.dependency_overrides[get_db] = override_get_db

# fake data

chara1 = Character(
    name="fakename1",
    status=StatusEnum.alive,
    species="Human",
    character_type="",
    gender=GenderEnum.male,
)
chara2 = Character(
    name="fakename2",
    status=StatusEnum.dead,
    species="Human",
    character_type="",
    gender=GenderEnum.female,   
)
chara3 = Character(
    name="fakename3",
    status=StatusEnum.dead,
    species="Human",
    character_type="",
    gender=GenderEnum.male,
)
now = datetime.now().date()
yesterday = now-timedelta(days=1)
str_now = now.strftime("%Y-%m-%d")
now = datetime.strptime(str_now, "%Y-%m-%d")
str_yesterday = yesterday.strftime("%Y-%m-%d")
yesterday = datetime.strptime(str_yesterday, "%Y-%m-%d")

def get_season_ep_number(season_ep):
    '''Returns an int season number and int episode number from string "S##E##"'''
    try:
        split_episode = season_ep.split("E")
        season_string = split_episode[0]
        episode_string = split_episode[-1]
        # method to only keep digits form the string
        season_int = int(''.join(c for c in season_string if c.isdigit()))
        episode_int = int(''.join(c for c in episode_string if c.isdigit()))
    except Exception as e:
        print(e)
        return None, None

    return season_int, episode_int

season_number1, episode_number1 = get_season_ep_number("S01E01")
season_number2, episode_number2 = get_season_ep_number("S01E02")
season_number3, episode_number3 = get_season_ep_number("S02E01")
ep1 = Episode(title="faketitle1",
    air_date=yesterday,
    episode_number=episode_number1,
    season_number=season_number1)
ep2 = Episode(title="faketitle2",
    air_date=yesterday,
    episode_number=episode_number2,
    season_number=season_number2)
ep3 = Episode(title="faketitle3",
    air_date=yesterday,
    episode_number=episode_number3,
    season_number=season_number3)

appearance1 = Appearance(episode_id=1, character_id=1)
appearance2 = Appearance(episode_id=3, character_id=2)

session = TestingSessionLocal()
session.add(ep1)
session.add(ep2)
session.add(ep3)
session.add(chara1)
session.add(chara2)
session.add(chara3)
session.add(appearance1)
session.add(appearance2)
session.commit()

client = TestClient(main.app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}



# Episodes ------------------------------------------------------------
def test_read_episodes():
    response = client.get("/api/v1/episodes")
    assert response.status_code == 200
    assert len(response.json()) == 3

    response = client.get(f"/api/v1/episodes?season_number=2&before_air_date={str_now}&character_name=fakename2")
    assert response.status_code == 200
    expected = [{
        "id": 3,
        "title": "faketitle3",
        "air_date": str_yesterday,
        "episode_number": 1,
        "season_number": 2
    }]
    assert response.json() == expected



# Characters ------------------------------------------------------------
def test_read_characters():
    response = client.get("/api/v1/characters")
    assert response.status_code == 200
    assert len(response.json()) == 3
    
    response = client.get(f"/api/v1/characters?gender=male&episode_name=faketitle1")
    expected = [{
        "id": 1,
        "name": "fakename1",
        "status": "alive",
        "species": "Human",
        "character_type": "",
        "gender": "male"
    }]
    assert response.status_code == 200
    assert response.json() == expected



# Users & Authentication -------------------------------------------------------------
def test_create_user():
    response = client.post(
        "/api/v1/signup",
        json={
            "id": 1,
            "username": "myusername",
            "email": "user@example.com",
            "password": "string"
        }
    )
    assert response.status_code == 201
    assert response.json()["username"] == "myusername"

    # test with same email
    response = client.post(
        "/api/v1/signup",
        json={
            "id": 1,
            "username": "myusername2",
            "email": "user@example.com",
            "password": "string"
        }
    )
    assert response.status_code == 400

@pytest.fixture(scope='function')
def create_test_user():

    '''fixture function to create a test user without actually testing the creation,
    but for the purpose of later tests'''

    test_username = "test_user"
    test_password = "test_password"
    response = client.get("/api/v1/users?username=test_user")

    #only create user if it doesn't exist yet
    if len(response.json()) < 1:
        
        response = client.post(
            "/api/v1/signup",
            json={
                "id": 1,
                "username": test_username,
                "email": "test_user@example.com",
                "password": test_password
            }
    )

    return test_username, test_password


@pytest.fixture(scope='function')
def create_test_access_token(create_test_user):

    '''fixture function to authenticate the test user without actually authenticating,
    but for the purpose of later tests'''

    test_username, test_password = create_test_user
    response = client.post(
            "/api/v1/token",
            data={
                "username": test_username,
                "password": test_password
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    token = "Bearer " + response.json()["access_token"]
    auth_header = {"Authorization": token}

    return auth_header

# no need to test the actual login with test_user since our fixture will
# but we still test for erroneous requests
def test_login_for_access_token():
    response = client.post(
            "/api/v1/token",
            data={
                "username": "nonexistant_user",
                "password": "string"
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
    assert response.status_code == 401

    response = client.post(
            "/api/v1/token",
            data={
                "username": "test_user",
                "password": "wrong_password"
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
    assert response.status_code == 401



def test_read_users():
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    assert len(response.json()) == 1


# now we can use our fixture to create the user and get the token
def test_read_user_self(create_test_access_token):
    response = client.get("/api/v1/users/me",
    headers=create_test_access_token)

    assert response.status_code == 200


def test_update_user_self(create_test_access_token):
    response = client.put("/api/v1/users/me",
    json={
        "email": "new_email_test_user@example.com"
    },
    headers=create_test_access_token)

    assert response.status_code == 200
    assert response.json()["email"] == "new_email_test_user@example.com"

    # try with same email than fake user created earlier
    response = client.put("/api/v1/users/me",
    json={
        "email": "user@example.com"
    },
    headers=create_test_access_token)

    assert response.status_code == 400


def test_update_user():
    response = client.put("/api/v1/users",
    json={
        "id": 1,
        "password": "new_password"
    })

    assert response.status_code == 200

    # try with no id
    response = client.put("/api/v1/users",
    json={
        "password": "new_password"
    })

    assert response.status_code == 422


def test_delete_user():
    response = client.delete("/api/v1/users?id=1")
    assert response.status_code == 204

    # try with nonexistent id
    response = client.delete("/api/v1/users?id=23")
    assert response.status_code == 404




# Comments ------------------------------------------------------------
def test_create_comments(create_test_access_token):
    # Create comment on one episode but without being authenticated
    response = client.post(
        "/api/v1/comments",
        json={
            "content": "this is comment 1",
            "episode_id": ep1.id,
        }
    )
    assert response.status_code == 401


    # Create comment on one episode
    response = client.post(
        "/api/v1/comments",
        json={
            "content": "this is comment 1",
            "episode_id": ep1.id,
            "user_id": 0
        },
    headers=create_test_access_token
    )
    assert response.status_code == 201
    assert response.json()["content"] == "this is comment 1"
    assert response.json()["episode_id"] == ep1.id
    assert not response.json()["character_id"]

    # Create comment on one character
    response = client.post(
        "/api/v1/comments",
        json={
            "content": "this is comment 2",
            "character_id": chara1.id,
            "user_id": 0
        },
    headers=create_test_access_token
    )
    assert response.status_code == 201
    assert response.json()["content"] == "this is comment 2"
    assert not response.json()["episode_id"]
    assert response.json()["character_id"] == chara1.id
    # Create comment on one episode+character
    response = client.post(
        "/api/v1/comments",
        json={
            "content": "this is comment 3",
            "episode_id": ep1.id,
            "character_id": chara1.id,
            "user_id": 0
        },
    headers=create_test_access_token
    )
    assert response.status_code == 201
    assert response.json()["content"] == "this is comment 3"
    assert response.json()["episode_id"] == ep1.id
    assert response.json()["character_id"] == chara1.id
    # Create comment on no episodes or characters should fail
    response = client.post(
        "/api/v1/comments",
        json={
            "content": "this is comment 4",
            "user_id": 0
        },
    headers=create_test_access_token
    )
    assert response.status_code == 400

    # test that we have indeed 3 comments
    assert session.query(Comment).count() == 3


def test_read_own_comments(create_test_access_token):
    response = client.get("/api/v1/users/me/comments",
    headers=create_test_access_token)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_read_comments():
    response = client.get("/api/v1/comments")
    assert response.status_code == 200
    assert len(response.json()) == 3

    response = client.get(f"/api/v1/comments?episode_id=1")
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = client.get(f"/api/v1/comments?user_id=2")
    assert response.status_code == 200
    assert len(response.json()) == 3

    response = client.get(f"/api/v1/comments?episode_id=1&character_id=1")
    assert response.status_code == 200
    expected = [{
        "id": 3,
        "content": "this is comment 3",
        "episode_id": 1,
        "character_id": 1,
        "user_id": 2
    }]
    assert response.json() == expected



# @app.put("/api/v1/comments/{id}", response_model=schemas.Comment)
def test_update_comment():
    response = client.put("/api/v1/comments/1",
    json={
        "content": "new content"
    })

    assert response.status_code == 200
    assert session.query(Comment.content).filter(Comment.id == 1).first().content == "new content"

    # try updating something else than content
    response = client.put("/api/v1/comments/1",
    json={
        "episode_id": 2
    })

    assert response.status_code == 422


def test_delete_comment():
    response = client.delete("/api/v1/comments/1")
    assert response.status_code == 204

    # try with nonexistent id
    response = client.delete("/api/v1/comments/54")
    assert response.status_code == 404


def test_export_comments():
    response = client.get("/api/v1/comments/export_csv")
    assert response.status_code == 200


def test_delete_user_self(create_test_access_token):
    response = client.delete("/api/v1/users/me", headers=create_test_access_token)
    assert response.status_code == 204
