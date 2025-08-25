# core/users/routs.py
from fastapi import status, HTTPException, Path, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.db import get_db
from users.models import UserModel
from fastapi import APIRouter
from math import ceil
from users.schemas import *


router = APIRouter(tags=["users"], prefix="/users")


@router.post("/login")
def user_login(payload: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(username=payload.username.lower()).first()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username doesnt exists!")
    if not user_obj.verify_password(payload.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password is invalid!")
        
    return []


@router.post("/register")
def user_register(payload: UserRegisterSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(username=payload.username.lower()).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already exists!")
        
    user_obj = UserModel(username=payload.username.lower())
    user_obj.set_password(payload.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    content={"detail": "user created",
             "id": user_obj.id,
             "username": user_obj.username}
    return JSONResponse(content=content)