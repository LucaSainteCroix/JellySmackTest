from datetime import date, datetime
import json
from sqlalchemy.exc import OperationalError

from database.database import Base, SessionLocal, engine
from models.models import Episode, Character, Appearance

# if tables already existed, delete them
try:
    Episode.__table__.drop(engine)
    Character.__table__.drop(engine)
    Appearance.__table__.drop(engine)
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
        date = datetime.strptime(episode_["air_date"], "%B %d, %Y")
        split_episode = episode_["episode"].split("E")
        season_string = split_episode[0]
        episode_string = split_episode[-1]
        # method to only keep digits form the string
        season_int = int(''.join(c for c in season_string if c.isdigit()))
        episode_int = int(''.join(c for c in episode_string if c.isdigit()))

        row = Episode(
            id=episode_["id"],
            title=episode_["name"],
            air_date=date,
            episode_number=episode_int,
            season_number=season_int
        )
        session.add(row)
    except Exception as e:
        print(e)
        pass
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
        character_type=character["type"],
        gender=character["gender"].lower(),
    )
    session.add(row)

    # Add the links between characters and episodes
    for episode in character["episode"]:
        link = Appearance(episode_id=episode, character_id=row.id)
        session.add(link)

session.commit()