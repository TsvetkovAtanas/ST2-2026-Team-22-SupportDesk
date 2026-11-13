from fastapi import Depends 
from sqlalchemy import select 
from sqlalchemy.exc import IntegrityError   # catching the duplicate email on commit
from sqlalchemy.orm import Session 

from app.db import get_db 
from app.models import Customer 
from app.schemas.customer import CustomerIn 


class DuplicateEmailError(Exception):
    """Raised when a customer with the same email already exists."""

class CustomerHasTicketsError(Exception):
    """Raised when deleting a customer who still has tickets."""

class CustomerRepository:
    """Repository pattern: the single access point for Customer data.

    Controllers never touch SQL or the session; database errors are
    translated into domain errors. Each write method commits its own
    transaction: simple, but calls cannot be grouped atomically.
    """


    def __init__(self, db: Session):
        self.db = db
    
    def get(self, customer_id: int) -> Customer | None:
        return self.db.get(Customer, customer_id)

    def list_all(self) -> list[Customer]:
        return list(self.db.scalars(select(Customer).order_by(Customer.name)).all())

    def create(self, data: CustomerIn) -> Customer:
        customer = Customer(**data.model_dump())
        try:
            self.db.add(customer)
            self.db.commit()
            self.db.refresh(customer)
        except IntegrityError:
            self.db.rollback()
            raise DuplicateEmailError()

        return customer

    def update(self, customer: Customer, data: CustomerIn) -> Customer:
        for key, value in data.model_dump().items():
            setattr(customer, key, value)
        try:
            self.db.commit()
            self.db.refresh(customer)
        except IntegrityError:
            self.db.rollback()
            raise DuplicateEmailError()

        return customer

    def delete(self, customer: Customer) -> None:
        try:
            self.db.delete(customer)
            self.db.commit()
                    
        except IntegrityError:
            self.db.rollback()
            raise CustomerHasTicketsError()


def get_customer_repository(db: Session = Depends(get_db)) -> CustomerRepository:
    return CustomerRepository(db)