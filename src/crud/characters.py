from sqlalchemy.orm import Session
from models.characters import Character

def get_characters(db: Session):
    return db.query(Character).all()