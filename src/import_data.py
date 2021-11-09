from datetime import date
from datetime import datetime
from sqlalchemy import Column,Sequence, Integer, String, MetaData
from database.database import Base, SessionLocal, engine
import json
from sqlalchemy.exc import OperationalError

from models.episodes import Episode
from models.characters import Character
from models.appeared_in import AppearedIn

# if tables already existed, delete them
try:
    Episode.__table__.drop(engine)
    Character.__table__.drop(engine)
    AppearedIn.__table__.drop(engine)
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
    date = datetime.strptime(episode_["air_date"], "%B %d, %Y")
    row = Episode(
        id=episode_["id"],
        title=episode_["name"],
        air_date=date,
        episode=episode_["episode"]
    )
    session.add(row)
session.commit()


# Import characters
print("Now importing Characters")
characters = {}
with open("data/rick_morty-characters_v1.json") as f:
    characters = json.load(f)

for i, character in enumerate(characters):
    row = Character(
        id=character["id"],
        name=character["name"],
        status=character["status"].lower(),
        species=character["species"],
        type=character["type"],
        gender=character["gender"].lower(),
    )
    session.add(row)

    # Add the links between characters and episodes
    for episode in character["episode"]:
        link = AppearedIn(episode_id=episode, character_id=row.id)
        session.add(link)

session.commit()