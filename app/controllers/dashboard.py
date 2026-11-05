from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

views = Jinja2Templates(directory='views')


router.get('/')
async def home_screen(request: Request):
    return views.TemplateResponse('dashboard.html', {'request': request})
