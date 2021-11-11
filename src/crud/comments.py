from sqlalchemy.orm import Session
from models.models import Comment
from schemas.schemas import CommentCreate


def get_comments(db: Session,
    episode: int = None,
    character: int = None,
    skip: int = 0,
    limit: int = 25
):
    query = db.query(Comment)
    if episode:
        query = query.filter(Comment.episode_id == episode)
    if character:
        query = query.filter(Comment.character_id == character)

    return query.offset(skip).limit(limit).all()


def create_comment(db: Session, comment: CommentCreate):

    db_comment = Comment(
        content=comment.content,
        episode_id=comment.episode_id,
        character_id=comment.character_id,
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
    """
    Delete a comment from the database with its id.
    """
    deletion = db.query(Comment).filter(Comment.id == comment_id).delete()
    db.commit()
    if not deletion:
        return None

    return deletion