# core/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.routs import router as tasks_router
from users.routs import router as users_router
from users.models import UserModel

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
app.include_router(users_router, prefix="/api/v1")




from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from fastapi import Depends
from auth.basic_auth import get_authenticated_user


security = HTTPBasic()

@app.get("/public",)
def public_rout():
    return {"detail": "this is public rout"}


@app.get("/private",)
def private_rout(user: UserModel = Depends(get_authenticated_user)):
    print(user)
    return {"detail": "this is private rout"}