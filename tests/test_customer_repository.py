import pytest
from app.repositories.customer_repository import CustomerRepository, DuplicateEmailError, CustomerHasTicketsError
from app.schemas.customer import CustomerIn
from app.schemas.ticket import TicketIn
from app.repositories.ticket_repository import TicketRepository

def make_data(**overrides):
    """Valid customer data; pass keyword arguments to change any field."""
    fields = {"name": "Ivan", "email": "ivan@test.com", "phone_number": None, "company": "ACME"}
    fields.update(overrides)
    return CustomerIn(**fields)

def make_ticket(customer, agent, **overrides):
    fields = {
        "title": "Cannot log in",
        "description": "Password reset email never arrives.",
        "customer_id": customer.id,
        "assigned_agent_id": agent.id,
    }
    fields.update(overrides)
    return TicketIn(**fields)


def test_create_returns_customer_with_id(db):
    repo = CustomerRepository(db)
    customer = repo.create(make_data())
    assert customer.id is not None
    assert customer.name == "Ivan"


def test_existing_id_returns_customer(db):
    repo = CustomerRepository(db)
    new_customer = repo.create(make_data())
    customer = repo.get(new_customer.id)
    assert customer is not None
    assert customer.id == new_customer.id

def test_missing_id_returns_none(db):
    repo = CustomerRepository(db)
    customer = repo.get(999)
    assert customer is None

def test_list_all_returns_every_customer_sorted_by_name(db):
    repo = CustomerRepository(db)
    customer1 = repo.create(make_data(name= "Zoran"))
    customer2 = repo.create(make_data(name= "Anna", email= "anna@test.com", phone_number= None, company= "ACME 2"))
    customers_list = repo.list_all()
    assert [c.name for c in customers_list] == ["Anna", "Zoran"] 

def test_update_changes_fields(db):
    repo = CustomerRepository(db)
    customer = repo.create(make_data())
    customer_updated = repo.update(customer, make_data(name= "Anna", email= "anna@test.com"))
    assert customer_updated.name == "Anna" and customer_updated.email == "anna@test.com"

def test_delete_removes_customer(db):
    repo = CustomerRepository(db)
    customer = repo.create(make_data())
    saved_id = customer.id
    repo.delete(customer)
    assert repo.get(saved_id) is None

def test_creating_customers_with_same_emails_raises_exception(db):
    repo = CustomerRepository(db)
    repo.create(make_data())
    with pytest.raises(DuplicateEmailError):
        repo.create(make_data(name="Zoro"))

def test_deleting_customer_with_ticket(db, customer, agent):
    repo = TicketRepository(db)
    repo_customer = CustomerRepository(db)
    repo.create(make_ticket(customer, agent))
    with pytest.raises(CustomerHasTicketsError):
        repo_customer.delete(customer)   

        
