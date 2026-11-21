import pytest
from pydantic import ValidationError
from app.schemas.customer import CustomerIn


def test_blank_phone_becomes_none():
    data = CustomerIn(name="Ivan", email="ivan@test.com", phone_number="   ", company="ACME")
    assert data.phone_number is None

def test_space_only_name_raises_exception():
    with pytest.raises(ValidationError):
        CustomerIn(name="    ", email="iva@test.com", phone_number="0878100200", company="Aatre Inc.")


def test_invalid_email_raises_exception():
    with pytest.raises(ValidationError):
        CustomerIn(name="Chocho", email="not-an-email", phone_number="0872323211", company="Company Ltd.")
