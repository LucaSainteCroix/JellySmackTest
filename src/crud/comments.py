from sqlalchemy.orm import Session

from models.models import Comment, User
from schemas.schemas import CommentCreate, User

def get_comments(db: Session,
    skip: int = 0,
    limit: int = 25,
    episode_id: int = None,
    character_id: int = None,
    user_id: int = None
):
    query = db.query(Comment)
    if episode_id:
        query = query.filter(Comment.episode_id == episode_id)
    if character_id:
        query = query.filter(Comment.character_id == character_id)
    if user_id:
        query = query.filter(Comment.user_id == user_id)

    return query.offset(skip).limit(limit).all()


def create_comment(db: Session, comment: CommentCreate, current_user: User):

    db_comment = Comment(
        content=comment.content,
        episode_id=comment.episode_id,
        character_id=comment.character_id,
        user_id=current_user.id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment


def update_comment(db: Session, comment_id: int, comment: CommentCreate):

    update = (
        db.query(Comment)
        .filter(Comment.id == comment_id)
        .update({Comment.content: comment.content})
    )
    db.commit()
    if not update:
        return None

    return db.query(Comment).filter(Comment.id == comment_id).first()


def delete_comment(db: Session, comment_id: int):

    deletion = db.query(Comment).filter(Comment.id == comment_id).delete()
    db.commit()
    if not deletion:
        return None

    return deletion