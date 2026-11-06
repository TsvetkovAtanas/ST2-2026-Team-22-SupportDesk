from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

views = Jinja2Templates(directory='app/views')


@router.get('/')
async def dashboard(request: Request):
    return views.TemplateResponse(
        request=request,
        name='dashboard.html',
        context={},
    )
