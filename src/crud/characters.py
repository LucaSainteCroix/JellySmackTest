from sqlalchemy.orm import Session

from models.models import Character, StatusEnum, GenderEnum

def get_characters(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    status: StatusEnum = None,
    species: str = None,
    character_type: str = None,
    gender: GenderEnum = None

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
        
    return query.offset(skip).limit(limit).all()