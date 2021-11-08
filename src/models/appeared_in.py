from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class AppearedIn(Base):

    __tablename__ = "appearedin"

    episode_id = Column(ForeignKey("episodes.id"), primary_key=True)
    character_id = Column(ForeignKey("characters.id"), primary_key=True)
    character = relationship("Character", back_populates="episodes")
    episode = relationship("Episode", back_populates="characters")