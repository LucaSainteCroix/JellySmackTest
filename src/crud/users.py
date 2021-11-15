from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException

from models.models import User
from schemas.schemas import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(
    db: Session,
    skip: int = 0,
    limit: int = 25,
    username: str = None
):
    query = db.query(User)
    if username:
        query = query.filter(User.username == username)

    return query.offset(skip).limit(limit).all()

def get_single_user(
    db: Session,
    username: str = None
):
    query = db.query(User)
    if username:
        query = query.filter(User.username == username)

    return query.first()

def create_user(db: Session, user: UserCreate):

    username_query = db.query(User).filter(User.username == user.username).first()
    if username_query:
        raise HTTPException(
            status_code=400,
            detail="An user with this username already exists in the system",
        )

    email_query = db.query(User).filter(User.email == user.email).first()
    if email_query:
        raise HTTPException(
            status_code=400,
            detail="An user with this email address already exists in the system",
        )

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        disabled=False
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def update_user(db: Session, user_to_update: UserUpdate, user_id: int):

    update = (
        db.query(User)
        .filter(User.id == user_id)
        .update({
            User.username: user_to_update.username,
            User.email: user_to_update.email,
            User.disabled: user_to_update.disabled,
            User.hashed_password: get_password_hash(user_to_update.password)})
    )
    db.commit()
    if not update:
        return None

    return db.query(User).filter(User.id == user_id).first()

def delete_user(db: Session, user_id: int):

    deletion = db.query(User).filter(User.id == user_id).delete()
    db.commit()
    if not deletion:
        return None

    return deletion