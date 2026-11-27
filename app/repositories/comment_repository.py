from fastapi import Depends
from sqlalchemy.orm import Session 

from app.db import get_db
from app.models.comment import Comment
from app.schemas.comment import CommentIn 


class CommentRepository:
    """Repository pattern: the single access point for Comment data."""

    def __init__(self, db: Session):
        self.db = db

    def get(self, comment_id: int) -> Comment | None:
        return self.db.get(Comment, comment_id)


    def create(self, ticket_id: int, author_agent_id: int, data: CommentIn) -> Comment:
        comment = Comment(ticket_id=ticket_id, author_agent_id=author_agent_id, **data.model_dump())

        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)

        return comment


    def delete(self, comment: Comment) -> None:
        self.db.delete(comment)
        self.db.commit()


def get_comment_repository(db: Session = Depends(get_db)) -> CommentRepository: 
    return CommentRepository(db)