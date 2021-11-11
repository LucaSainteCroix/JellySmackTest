from database.database import Base, SessionLocal, engine, get_db
from fastapi import FastAPI, Depends, HTTPException
from crud import episodes, characters, comments
from schemas import schemas
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Episodes ------------------------------------------------------------
@app.get("/api/v1/episodes", response_model=List[schemas.Episode])
def list_episodes(
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
        episode_number, season_number, character_name)


# Characters ------------------------------------------------------------
@app.get("/api/v1/characters", response_model=List[schemas.Character])
def list_characters(db: Session = Depends(get_db)):

	return characters.get_characters(db)


# Comments ------------------------------------------------------------
@app.get("/api/v1/comments", response_model=List[schemas.Comment])
def list_comments(db: Session = Depends(get_db)):

	return comments.get_comments(db)


@app.post("/api/v1/comments", response_model=schemas.Comment, status_code=201)
def create_comments(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db)
):
    if not comment.episode_id and not comment.character_id:
        raise HTTPException(
            status_code=400,
            detail="Episode ID or Character ID is required to create a comment",
        )

    return comments.create_comment(db, comment)


@app.put("/api/v1/comments/{id}", response_model=schemas.Comment)
def update_comment(
    id: int, comment: schemas.CommentUpdate, db: Session = Depends(get_db)
):
    comment = comments.update_comment(db, id, comment)
    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Could not find a comment to update",
        )
    return comment


@app.delete("/api/v1/comments/{id}", status_code=204)
def delete_comment(id: int, db: Session = Depends(get_db)):
    if not comments.delete_comment(db, id):
        raise HTTPException(
            status_code=404,
            detail="Could not find a comment to delete",
        )


# Home -------------------------------------------------------------
@app.get("/")
def home():
  	return {"msg": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)