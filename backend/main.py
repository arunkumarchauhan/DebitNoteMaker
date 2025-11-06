from fastapi import FastAPI
from sqlalchemy.orm import Session
from core.config import settings
from db.session import engine, Base
from db.base import *  # Import all models, so that they will be registered properly on the metadata. Otherwise, you will have to import them first before calling Base.metadata.create_all
from api import base_router
from app import base as app_route
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from app.template import templates

def create_tables():
    Base.metadata.create_all(bind=engine)
def indclude_router(app:Session):
    app.include_router(base_router.router)
    app.include_router(app_route.router)

@asynccontextmanager
async def startup_event(app:FastAPI):
    templates.env.filters["format_datetime"] = lambda dt, fmt: dt.strftime(fmt)
    yield

def configure_static_files(app:FastAPI):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def start_application():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION,lifespan=startup_event)
    configure_static_files(app=app)
    indclude_router(app=app)
    return app

app=start_application()
