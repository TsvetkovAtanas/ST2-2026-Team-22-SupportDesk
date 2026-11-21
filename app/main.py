from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.controllers import dashboard, customers


app = FastAPI()


app.mount('/static', StaticFiles(directory='app/static'), name='static')
app.include_router(dashboard.router)
app.include_router(customers.router)

