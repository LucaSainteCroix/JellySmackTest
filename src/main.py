from database.database import Base, SessionLocal, engine
from fastapi import FastAPI
from crud.characters import get_characters
from crud.episodes import get_episodes

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/episodes")
async def list_episodes():
	db = next(get_db())
	return get_episodes(db)

@app.get("/characters")
async def list_characters():
	db = next(get_db())
	return get_characters(db)

@app.get("/")
async def home():
  	return {"msg": "Hello World"}