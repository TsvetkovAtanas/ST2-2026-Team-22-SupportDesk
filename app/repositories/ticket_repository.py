from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.models import Ticket
from app.models.enums import Status, Priority
from app.schemas.ticket import TicketIn

class InvalidReferenceError(Exception):
    """Raised when a ticket refers to a customer or agent that does not exist."""

class TicketRepository:
    """Repository pattern: the single access point for Ticket data.
    
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, ticket_id: int) -> Ticket | None:
        return self.db.get(Ticket, ticket_id, options=[selectinload(Ticket.customer), selectinload(Ticket.agent), selectinload(Ticket.comments)])
    
    def list_all(self, status: Status | None = None, priority: Priority | None = None) -> list[Ticket]:
        stmt = select(Ticket).options(selectinload(Ticket.customer), selectinload(Ticket.agent))
        if status:
            stmt = stmt.where(Ticket.status == status)
        if priority:
            stmt = stmt.where(Ticket.priority == priority)
        stmt = stmt.order_by(Ticket.created_at.desc(), Ticket.id.desc())
        return list(self.db.scalars(stmt).all())

    def create(self, data: TicketIn) -> Ticket:
        ticket = Ticket(**data.model_dump())
        try:
            self.db.add(ticket)
            self.db.commit()
            self.db.refresh(ticket)
        except IntegrityError:
            self.db.rollback()
            raise InvalidReferenceError()
        return ticket

    def update(self, ticket: Ticket, data: TicketIn) -> Ticket:
        for key, value in data.model_dump().items():
            setattr(ticket, key, value)
        try:
            self.db.commit()
            self.db.refresh(ticket)
        except IntegrityError:
            self.db.rollback()
            raise InvalidReferenceError()
        return ticket

    def delete(self, ticket: Ticket) -> None:
        self.db.delete(ticket)
        self.db.commit()


def get_ticket_repository(db: Session = Depends(get_db)) -> TicketRepository:
    return TicketRepository(db)