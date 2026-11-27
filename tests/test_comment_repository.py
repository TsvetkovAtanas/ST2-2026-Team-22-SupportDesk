import pytest
from app.repositories.comment_repository import CommentRepository
from app.schemas.comment import CommentIn
from app.repositories.ticket_repository import TicketRepository


def make_comment(**overrides):
    fields = {
        "body": "I tried to fix the issue but at the end the password reset email never arrives."
    }
    fields.update(overrides)
    return CommentIn(**fields)

def test_create_comment(db, ticket, agent):
    repo = CommentRepository(db)
    comment = repo.create(ticket.id, agent.id, make_comment(body="New body"))
    assert comment.id is not None
    assert comment.body == "New body"

def test_cascade_comment_deletion(db, ticket, agent):
    repo = CommentRepository(db)
    repo_ticket = TicketRepository(db)
    comment = repo.create(ticket.id, agent.id, make_comment(body="New body"))
    comment_id = comment.id
    repo_ticket.delete(ticket)
    assert repo.get(comment_id) is None
