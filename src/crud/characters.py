from sqlalchemy.orm import Session

from models.models import Character, StatusEnum, GenderEnum, Episode, Appearance

def get_characters(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    status: StatusEnum = None,
    species: str = None,
    character_type: str = None,
    gender: GenderEnum = None,
    episode_name = None

):
    query = db.query(Character)
    if status:
        query = query.filter(Character.status == status.value)
    if species:
        query = query.filter(Character.species == species)
    if character_type:
        query = query.filter(Character.character_type == character_type)
    if gender:
        query = query.filter(Character.gender == gender.value)
    if episode_name:
        # Get episode id corresponding to the episode name sent (case insensitive search)
        episode_id_query = db.query(Episode.id).filter(Episode.title.ilike(episode_name))
        
        # Join Characters with Episodes with condition that episode_id is right
        query = query.join(Character.episode.and_(Appearance.episode_id.in_(episode_id_query)))

    return query.offset(skip).limit(limit).all()