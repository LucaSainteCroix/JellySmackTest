from fastapi import FastAPI, Depends, HTTPException
from http import HTTPStatus
from typing import List
from sqlalchemy.orm import Session
from datetime import date, timedelta
import uvicorn
from decouple import config
from fastapi.security import OAuth2PasswordRequestForm
import csv
import io
from fastapi.responses import StreamingResponse, Response

from auth.auth_handler import authenticate_user, create_access_token, get_current_active_user
from database.database import Base, engine, get_db
from crud import episodes, characters, comments, users
from schemas import schemas
from models.models import Comment, StatusEnum, GenderEnum


SECRET_KEY = config("secret")
ALGORITHM = config("algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default = 30)

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Episodes ------------------------------------------------------------
@app.get("/api/v1/episodes", response_model=List[schemas.Episode])
async def read_episodes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 25,
    before_air_date: date = None,
    after_air_date: date = None,
    episode_number: int = None,
    season_number: str = None,
    character_name: str = None
):
    return episodes.get_episodes(
        db, skip, limit, before_air_date, after_air_date,
        episode_number, season_number, character_name
    )



# Characters ------------------------------------------------------------
@app.get("/api/v1/characters", response_model=List[schemas.Character])
async def read_characters(db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 25,
    status: StatusEnum = None,
    species: str = None,
    character_type: str = None,
    gender: GenderEnum = None,
    episode_name: str = None
):

    return characters.get_characters(
        db, skip, limit, status, species, character_type, gender, episode_name
    )



# Comments ------------------------------------------------------------
@app.get("/api/v1/comments", response_model=List[schemas.Comment])
async def read_comments(db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 25,
    episode_id: int = None,
    character_id: int = None,
    user_id: int = None
):

    return comments.get_comments(
         db, skip, limit, episode_id, character_id, user_id
    )


@app.get("/api/v1/users/me/comments", response_model=List[schemas.Comment])
async def read_own_comments(db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    return comments.get_comments(db, user_id = current_user.id)


@app.post("/api/v1/comments", response_model=schemas.Comment, status_code=201)
async def create_comments(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    if not comment.episode_id and not comment.character_id:
        raise HTTPException(
            status_code=400,
            detail="Episode ID or Character ID is required to create a comment",
        )

    return comments.create_comment(db, comment, current_user)


@app.put("/api/v1/comments/{id}", response_model=schemas.Comment)
async def update_comment(
    id: int, comment: schemas.CommentUpdate, db: Session = Depends(get_db)
):
    updated_comment = comments.update_comment(db, id, comment)
    if not updated_comment:
        raise HTTPException(
            status_code=404,
            detail="Could not find a comment to update",
        )
    return updated_comment


@app.delete("/api/v1/comments/{id}", status_code=204)
async def delete_comment(id: int, db: Session = Depends(get_db)):
    if not comments.delete_comment(db, id):
        raise HTTPException(
            status_code=404,
            detail="Could not find a comment to delete",
        )
    return Response(status_code=HTTPStatus.NO_CONTENT.value)


@app.get("/api/v1/comments/export_csv")
async def export_comments(db: Session = Depends(get_db)):

    '''Export all comments as csv file'''

    all_comments = db.query(Comment).all()
    if len(all_comments) == 0:
        raise HTTPException(
            status_code=404,
            detail="No Comments to export",
        )
    all_comments_dicts = []
    # convert row objects to dicts and remove instance state element
    for c in all_comments:
        row_dict = c.__dict__
        row_dict.pop("_sa_instance_state")
        all_comments_dicts.append(row_dict)

    keys = all_comments_dicts[0].keys()
    stream = io.StringIO()
    dict_writer = csv.DictWriter(stream, keys)
    dict_writer.writeheader()
    dict_writer.writerows(all_comments_dicts)

    response = StreamingResponse(iter([stream.getvalue()]),
                        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = "attachment; filename=comments_export.csv"

    return response


# Authentication -------------------------------------------------------------
@app.post("/api/v1/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):

    '''Returns JWT access_token when user inputs valid username and password for existant and active user'''

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



# Users -------------------------------------------------------------
@app.get("/api/v1/users", response_model=List[schemas.User])
async def read_users(
    skip: int = 0,
    limit: int = 25,
    username: str = None,
    db: Session = Depends(get_db)
):
    return users.get_user(db, skip, limit, username)


@app.get("/api/v1/users/me", response_model=schemas.User)
async def read_user_self(current_user: schemas.User = Depends(get_current_active_user)):
    '''Returns User Instance of current user'''
    return current_user


@app.post("/api/v1/signup", response_model=schemas.User, status_code=201)
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return users.create_user(db, user)


@app.put("/api/v1/users/me", response_model=schemas.User)
async def update_user_self(
    user_to_update: schemas.UserUpdateSelf,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    updated_user = users.update_user(db, user_to_update, current_user.id)

    return updated_user


@app.delete("/api/v1/users/me", status_code=204)
async def delete_user_self(
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)):
    if not users.delete_user(db, current_user.id):
        raise HTTPException(
            status_code=404,
            detail="Could not delete your account",
        )
    return Response(status_code=HTTPStatus.NO_CONTENT.value)

@app.put("/api/v1/users", response_model=schemas.User)
async def update_user(
    user_to_update: schemas.UserUpdate,
    db: Session = Depends(get_db)
): 
    updated_user = users.update_user(db, user_to_update, user_to_update.id)

    return updated_user


@app.delete("/api/v1/users", status_code=204)
async def delete_user(
    id: int,
    db: Session = Depends(get_db)):
    if not users.delete_user(db, id):
        raise HTTPException(
            status_code=404,
            detail="Could not delete this account",
        )
    return Response(status_code=HTTPStatus.NO_CONTENT.value)


# Home -------------------------------------------------------------
@app.get("/")
async def home():
  	return {"msg": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)