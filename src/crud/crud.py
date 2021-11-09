from sqlalchemy.orm import Session
from models.models import Episode, Character, Comment

def get_episodes(db: Session):
    return db.query(Episode).all()


def get_characters(db: Session):
    return db.query(Character).all()


def get_comments(db: Session):
    return db.query(Comment).all()