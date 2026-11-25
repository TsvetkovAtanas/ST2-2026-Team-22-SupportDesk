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

def test_create_sets_defaults(db, customer, agent):
    repo = TicketRepository(db)
    ticket = repo.create(make_ticket(customer, agent))
    assert ticket.id is not None
    assert ticket.status == Status.OPEN
    assert ticket.priority == Priority.MEDIUM

def test_get_returns_the_ticket(db, customer, agent):
    repo = TicketRepository(db)
    ticket = repo.create(make_ticket(customer, agent))
    found = repo.get(ticket.id)
    assert found.id == ticket.id
    assert found.customer.name == customer.name

def test_get_999_return_none(db):
    repo = TicketRepository(db)
    assert repo.get(999) is None

def test_update_changes_title(db, customer, agent):
    repo = TicketRepository(db)
    ticket = repo.create(make_ticket(customer, agent))
    ticket = repo.update(ticket, make_ticket(customer, agent, title="Maruncho"))
    assert ticket.title == "Maruncho"

def test_delete_removes_ticket(db, customer, agent):
    repo = TicketRepository(db)
    ticket = repo.create(make_ticket(customer, agent))
    saved_id = ticket.id
    repo.delete(ticket)
    assert repo.get(saved_id) is None

def test_filtering(db, customer, agent):
    repo = TicketRepository(db)
    repo.create(make_ticket(customer, agent, priority=Priority.HIGH))
    repo.create(make_ticket(customer, agent, priority=Priority.LOW))
    result = repo.list_all(priority=Priority.HIGH)
    assert len(result) == 1
    assert result[0].priority == Priority.HIGH

def test_order(db, customer, agent):
    repo = TicketRepository(db)
    repo.create(make_ticket(customer, agent))
    ticket_new = repo.create(make_ticket(customer, agent))
    assert repo.list_all()[0].id == ticket_new.id

def test_create_with_id_999_raises_error(db, customer, agent):
    repo = TicketRepository(db)
    with pytest.raises(InvalidReferenceError):
            repo.create(make_ticket(customer, agent, customer_id=999))
