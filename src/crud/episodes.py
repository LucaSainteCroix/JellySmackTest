from sqlalchemy.orm import Session
from sqlalchemy import Date

from models.models import Episode, Appearance, Character


def get_episodes(
    db: Session,
    skip: int = 0,
    limit: int = 25,
    before_air_date: Date = None,
    after_air_date: Date = None,
    episode_number: int = None,
    season_number: str = None,
    character_name: str = None

):
    query = db.query(Episode)
    if before_air_date:
        query = query.filter(Episode.air_date < before_air_date)
    if after_air_date:
        query = query.filter(Episode.air_date > after_air_date)
    if episode_number:
        query = query.filter(Episode.episode_number == episode_number)
    if season_number:
        query = query.filter(Episode.season_number == season_number)
        # Search for episodes where a certain character is in
    if character_name:
        # Get character id corresponding to the character name sent (case insensitive search)
        character_id_query = db.query(Character.id).filter(Character.name.ilike(character_name))
        
        # Join Episodes with Characters with condition that character_id is right
        query = query.join(Episode.character.and_(Appearance.character_id.in_(character_id_query)))
       
    return query.offset(skip).limit(limit).all()