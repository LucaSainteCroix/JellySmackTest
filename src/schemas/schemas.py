from datetime import date
from pydantic import BaseModel
from models.models import GenderEnum, StatusEnum
from typing import Optional, List

# Episodes
class Episode(BaseModel):
    id: int
    title: str
    air_date: date
    episode_number: int
    season_number: int

    class Config:
        orm_mode = True


# Characters
class Character(BaseModel):
    id: int
    name: str
    status: StatusEnum
    species: str
    type: Optional[str] = ""
    gender: GenderEnum

    class Config:
        orm_mode = True


# Comments
class CommentBase(BaseModel):
    episode_id: Optional[int]
    character_id: Optional[int]
    content: str

class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True

class CommentUpdate(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass



