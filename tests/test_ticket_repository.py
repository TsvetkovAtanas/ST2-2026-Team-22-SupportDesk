import pytest
from app.models.enums import Priority, Status
from app.repositories.ticket_repository import TicketRepository, InvalidReferenceError
from app.schemas.ticket import TicketIn


def make_ticket(customer, agent, **overrides):
    fields = {
        "title": "Cannot log in",
        "description": "Password reset email never arrives.",
        "customer_id": customer.id,
        "assigned_agent_id": agent.id,
    }
    fields.update(overrides)
    return TicketIn(**fields)