from database.database import Base, SessionLocal, engine, get_db
from fastapi import FastAPI, Depends
from crud.crud import get_characters, get_episodes, get_comments


Base.metadata.create_all(bind=engine)

app = FastAPI()



@app.get("/api/v1/episodes")
async def list_episodes(db: SessionLocal = Depends(get_db)):
	
	return get_episodes(db)

@app.get("/api/v1/characters")
async def list_characters(db: SessionLocal = Depends(get_db)):

	return get_characters(db)

@app.get("/")
async def home():
  	return {"msg": "Hello World"}