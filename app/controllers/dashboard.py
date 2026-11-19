from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.templates import templates

router = APIRouter()


@router.get('/')
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='dashboard.html',
        context={},
    )
