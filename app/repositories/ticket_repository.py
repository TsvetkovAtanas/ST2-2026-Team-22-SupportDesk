from fastapi import Depends 
from sqlalchemy import select 
from sqlalchemy.orm import Session 

from app.db import get_db 
from app.models import Ticket 

class TicketRepository:
    """Repository pattern: the single access point for Ticket data.
    
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get(self, ticket_id: int) -> Ticket | None:
        return self.db.get(Ticket, ticket_id)
    
    def list_all(self, status=None, priority=None) -> list[Ticket]:
        return list(self.db.scalars(select(Ticket).order_by(Ticket.name)).all())

def get_ticket_repository(db: Session = Depends(get_db)) -> TicketRepository:
    return TicketRepository(db)