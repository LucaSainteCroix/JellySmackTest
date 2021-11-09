from datetime import date
from pydantic import BaseModel
from models.characters import GenderEnum, StatusEnum
from typing import Optional

class Episode(BaseModel):
    id: int
    title: str
    air_date: date
    episode_number: int
    season_number: int

    class Config:
        orm_mode = True


class Character(BaseModel):
    id: int
    name: str
    status: StatusEnum
    species: str
    type: Optional[str] = ""
    gender: GenderEnum

    class Config:
        orm_mode = True

