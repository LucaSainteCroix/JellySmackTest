import enum
from database.database import Base
from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship
from .appeared_in import AppearedIn

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
    name = Column(String, index=True)
    status = Column(Enum(StatusEnum))
    species = Column(String, default="")
    type = Column(String)
    gender = Column(Enum(GenderEnum))
    episodes = relationship(AppearedIn, back_populates="character")
