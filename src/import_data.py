from datetime import datetime
import json
from sqlalchemy.exc import OperationalError
import argparse

from database.database import Base, SessionLocal, engine
from models.models import Episode, Character, Appearance, Comment, User
from tests.test_main import get_season_ep_number


parser = argparse.ArgumentParser(description="Initialize database and add Episodes & Characters data")
parser.add_argument("-d", "--drop", action="store_true", help="Drop Comment and User tables")
parser.add_argument("-k", "--keep", action="store_true",
                    help="Keep Episode, Character and Appearance tables (deleted by default)")
args = parser.parse_args()

if not args.keep:
    try:
        Episode.__table__.drop(engine)
        Character.__table__.drop(engine)
        Appearance.__table__.drop(engine)
    except OperationalError:
        pass

if args.drop:
    try:
        Comment.__table__.drop(engine)
        User.__table__.drop(engine)
    except OperationalError:
        pass

Base.metadata.create_all(engine)

session = SessionLocal()

# Import episodes
print("Now importing Episodes")
episodes = {}
with open("data/rick_morty-episodes_v1.json") as f:
    episodes = json.load(f)


for i, episode_ in enumerate(episodes):
    try:
        air_date = datetime.strptime(episode_["air_date"], "%B %d, %Y")
        season_int, episode_int = get_season_ep_number(episode_["episode"])
        id_check_query = session.query(Episode).filter(Episode.id == episode_["id"]).count()
        if id_check_query == 0:
            row = Episode(
                id=episode_["id"],
                title=episode_["name"],
                air_date=air_date,
                episode_number=episode_int,
                season_number=season_int
            )
            session.add(row)
    except OperationalError:
        pass
session.commit()


# Import characters
print("Now importing Characters")
characters = {}
with open("data/rick_morty-characters_v1.json") as f:
    characters = json.load(f)

for i, character in enumerate(characters):
    id_check_query = session.query(Character).filter(Character.id == character["id"]).count()
    if id_check_query == 0:
        row = Character(
            id=character["id"],
            name=character["name"],
            status=character["status"].lower(),
            species=character["species"],
            character_type=character["type"],
            gender=character["gender"].lower(),
        )
        session.add(row)

        # Add characters appearances in episodes
        for episode in character["episode"]:
            appearance = Appearance(episode_id=episode, character_id=row.id)
            session.add(appearance)

session.commit()
