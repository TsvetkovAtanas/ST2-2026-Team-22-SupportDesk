from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from app.templates import templates
from app.schemas.customer import CustomerIn
from app.repositories.customer_repository import (
    CustomerRepository, get_customer_repository,
    DuplicateEmailError, CustomerHasTicketsError,
)


router = APIRouter(prefix="/customers")

Repo = Annotated[CustomerRepository, Depends(get_customer_repository)]

def render_form(request, customer, form, errors, status_code=200):
    return templates.TemplateResponse(
        request=request, name="customers/form.html",
        context={"customer": customer, "form": form, "errors": errors},
        status_code=status_code
    )


@router.get("")
def list_customers(request: Request, repo: Repo):
    customers = repo.list_all()
    return templates.TemplateResponse(
        request=request,
        name="customers/list.html",
        context={"customers": customers},
    )


@router.get("/new")
def new_customer_form(request: Request):
    return render_form(request, customer=None, form={}, errors={})


@router.post("")
def create_customer(
    request: Request, 
    repo: Repo, 
    name: Annotated[str, Form()] = "",
    email: Annotated[str, Form()] = "",
    phone_number: Annotated[str, Form()] = "",
    company: Annotated[str, Form()] = ""):

    form = {"name": name, "email": email, "phone_number": phone_number, "company": company}

    try:
        data = CustomerIn(**form)
        repo.create(data)
    except ValidationError as e:
        errors = {err["loc"][0]: err["msg"] for err in e.errors()}        
        return render_form(request, None, form, errors, status_code=400)
    except DuplicateEmailError:
        return render_form(request, None, form, {"email": "Email already exists"}, status_code=400)

    return RedirectResponse("/customers", status_code=303)


@router.get("/{customer_id}/edit")
def edit_form(request: Request, repo:Repo, customer_id: int):

    customer = repo.get(customer_id)
    if customer is None:
        raise HTTPException(status_code=404)

    form = {
        "name": customer.name,
        "email": customer.email,
        "phone_number": customer.phone_number,
        "company": customer.company,
    }

    return render_form(request, customer, form, {})


@router.post("/{customer_id}")
def update_customer(request: Request, repo: Repo, customer_id: int, 
    name: Annotated[str, Form()] = "",
    email: Annotated[str, Form()] = "",
    phone_number: Annotated[str, Form()] = "",
    company: Annotated[str, Form()] = "",):

    customer = repo.get(customer_id)
    if customer is None:
        raise HTTPException(status_code=404)
    
    form = {"name": name, "email": email, "phone_number": phone_number, "company": company}
    try:
        data = CustomerIn(**form)
        repo.update(customer, data)
    except ValidationError as e:
        errors = {err["loc"][0]: err["msg"] for err in e.errors()}        
        return render_form(request, customer, form, errors, status_code=400)
    except DuplicateEmailError:
        return render_form(request, customer, form, {"email": "Email already exists"}, status_code=400)

    return RedirectResponse("/customers", status_code=303)


@router.post("/{customer_id}/delete")
def delete_customer(customer_id: int, repo: Repo):
    customer = repo.get(customer_id)
    if customer is None:
        raise HTTPException(status_code=404)

    try:
        repo.delete(customer)
    except CustomerHasTicketsError:
        return RedirectResponse("/customers?error=has_tickets", status_code=303)
    return RedirectResponse("/customers", status_code=303)