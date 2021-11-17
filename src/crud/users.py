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

    return db_user


def update_user(db: Session, user_to_update: UserUpdate, user_id: int):
    query = db.query(User).filter(User.id == user_id)
    query_count = query.count()

    if query_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Could not update this account, account not found",
        )
    user_info = query.first()
    # verify the "to be updated" fields exist and are not the same as they are already in the database
    if user_to_update.username and user_info.username != user_to_update.username:
        # verify the username doesn't already exist
        username_query = db.query(User).filter(User.username == user_to_update.username).first()
        if username_query  :
            raise HTTPException(
                status_code=400,
                detail="An user with this username already exists in the system",
            )
        update = query.update({User.username: user_to_update.username})
    
    if user_to_update.email and user_info.email != user_to_update.email:
        # verify the email doesn't already exist
        email_query = db.query(User).filter(User.email == user_to_update.email).first()
        if email_query:
            raise HTTPException(
                status_code=400,
                detail="An user with this email address already exists in the system",
            )
        update = query.update({User.email: user_to_update.email})

    if user_to_update.disabled:
        update = query.update({User.disabled: user_to_update.disabled})

    if user_to_update.password:
        update = query.update({User.hashed_password: get_password_hash(user_to_update.password)})

    db.commit()
    return db.query(User).filter(User.id == user_id).first()


def delete_user(db: Session, user_id: int):

    deletion = db.query(User).filter(User.id == user_id).delete()
    db.commit()
    if not deletion:
        return None

    return deletion