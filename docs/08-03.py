# to change interptreter in VSCode >
#                       Ctrl+Shift+P
#                       and enter Python: Select Interpreter
#                       and enter python.exe path in .venv folder
#                  e.g. F:\Git-Repository\FastAPI-ToDo-app\core\.venv\Scripts\python.exe


# set up main.py
"""
# core/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Startup")
    yield
    print("Application Shutdown")
    

app = FastAPI(lifespan=lifespan)

"""

# set config.py file
"""
# core/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
"""

# add .env and .env.sample file
# SQLALCHEMY_DATABASE_URL = sqlite:///./sqlite.db



# for connection database with sqlite > create db.py and set it up
"""
# core/core/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""



# create routs for tasks
"""
# core/tasks/routs.py
from fastapi import APIRouter

router = APIRouter(tags=["tasks"], prefix="/todo")


@router.get("/tasks")
async def retrieve_tasks_list():
    return []


@router.get("/tasks/{task_id}")
async def retrieve_task_detail(task_id : int):
    return []
"""


# and import rout from tasks in main.py
"""
# core/main.py
from tasks.routs import router as tasks_router

app.include_router(tasks_router, prefix="/api/v1")
"""


# and add tags in main.py for project informations
"""
# core/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.routs import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Startup")
    yield
    print("Application Shutdown")
    
tags_metadata = [
    {
        "name": "tasks",
        "descriptions" : "Operations related to task management",
        "externalDocs" : {
            "description" : "More about tasks",
            "url" : "http://127.0.0.1:8000/docs/tasks"
        }
    }
]


app = FastAPI(
    title="ToDo-App",
    description="This is a ToDo app",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Poorya Fayazi",
        "url": "https://itmeter.ir/about",
        "email": "poorya189@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan, openapi_tags=tags_metadata)

app.include_router(tasks_router, prefix="/api/v1")
"""


