import enum
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy import Column, Enum, Date, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from database.database import Base


class Appearance(Base):
    '''Association Class for the many-to-many relationship between episodes and characters'''
    __tablename__ = "appearances"

    episode_id = Column(ForeignKey("episodes.id"), primary_key=True)
    character_id = Column(ForeignKey("characters.id"), primary_key=True)
    character = relationship("Character", back_populates="episode")
    episode = relationship("Episode", back_populates="character")


class Episode(Base):

    __tablename__ = "episodes"

    id = Column(Integer, index=True, primary_key=True)
    title = Column(String, index=True)
    air_date = Column(Date)
    episode_number = Column(Integer, default=0)
    season_number = Column(Integer, default=0)

    character = relationship(Appearance, back_populates="episode")


class StatusEnum(str, enum.Enum):
    alive = "alive"
    dead = "dead"
    unknown = "unknown"


class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    genderless = "genderless"
    unknown = "unknown"


class Character(Base):

    __tablename__ = "characters"

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String(255), index=True)
    status = Column(Enum(StatusEnum))
    species = Column(String, default="")
    character_type = Column(String)
    gender = Column(Enum(GenderEnum))
    episode = relationship(Appearance, back_populates="character")


class Comment(Base):

    __tablename__ = "comments"
    __table_args__ = (
            CheckConstraint('NOT(episode_id IS NULL AND character_id IS NULL)'),
            )
        
    id = Column(Integer, index=True, primary_key=True)
    content = Column(String)
    episode_id = Column(ForeignKey("episodes.id"), nullable=True)
    character_id = Column(ForeignKey("characters.id"), nullable=True)
    user_id = Column(ForeignKey("users.id"))


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, index=True, primary_key=True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default = False)
