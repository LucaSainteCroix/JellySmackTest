from sqlalchemy.orm import Session
from models.episodes import Episode

def get_episodes(db: Session):
    return db.query(Episode).all()