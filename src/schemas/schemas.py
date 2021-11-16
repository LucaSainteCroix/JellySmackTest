from datetime import date
from pydantic import BaseModel, EmailStr
from typing import Optional, List

from models.models import GenderEnum, StatusEnum


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
    character_type: Optional[str] = ""
    gender: GenderEnum

    class Config:
        orm_mode = True


# Comments
class CommentBase(BaseModel):
    episode_id: Optional[int]
    character_id: Optional[int]
    content: str
    user_id: int


class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True


class CommentUpdate(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


# Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Users
class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    disabled: Optional[bool] = False

    class Config:
        orm_mode = True

class UserCreate(User):
    password: str

class UserUpdateSelf(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    disabled: Optional[bool] = False
    password: Optional[str]

class UserUpdate(UserUpdateSelf):
    id: int