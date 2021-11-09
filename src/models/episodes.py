from database.database import Base
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship
from .appeared_in import AppearedIn
    

class Episode(Base):

    __tablename__ = "episodes"

    id = Column(Integer, index=True, primary_key=True)
    title = Column(String, index=True)
    air_date = Column(Date)
    episode = Column(String)
    characters = relationship(AppearedIn, back_populates="episode")
