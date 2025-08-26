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



# Basic Authentication
"""
from fastapi.security import HTTPBasic
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
"""


# APIKeyHeader
"""
from fastapi.security import APIKeyHeader
from fastapi import Depends

header_scheme = APIKeyHeader(name="x-key")

@app.get("/public",)
def public_rout():
    return {"detail": "this is public rout"}


@app.get("/private",)
def private_rout(api_key = Depends(header_scheme)):
    print(api_key)
    return {"detail": "this is private rout"}
"""


# APIKeyQuery
"""
from fastapi import Depends
from fastapi.security import APIKeyQuery


query_scheme = APIKeyQuery(name="api_key")


@app.get("/public",)
def public_rout():
    return {"detail": "this is public rout"}


@app.get("/private",)
def private_rout(api_key = Depends(query_scheme)):
    print(api_key)
    return {"detail": "this is private rout"}
"""



# HTTPBearer Authentication

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends
from auth.token_auth import get_authenticated_user
security = HTTPBearer()


@app.get("/public",)
def public_rout():
    return {"detail": "this is public rout"}


@app.get("/private",)
def private_rout(user = Depends(get_authenticated_user)):
    return {"detail": "this is public rout" , "username": user.username}