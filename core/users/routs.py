# core/users/routs.py
from fastapi import status, HTTPException, Path, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.db import get_db
from users.models import UserModel, TokenModel
from fastapi import APIRouter
from math import ceil
from users.schemas import *
import secrets
from sqlalchemy import desc

router = APIRouter(tags=["users"], prefix="/users")


def generate_token(length=32):
    return secrets.token_hex(length)


@router.post("/login")
def user_login(payload: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(username=payload.username.lower()).first()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username doesnt exists!")
    if not user_obj.verify_password(payload.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password is invalid!")
    
    token_obj = (db.query(TokenModel)
        .filter(TokenModel.user_id == user_obj.id)
        .order_by(desc(TokenModel.create_date))
        .first())
    
    if token_obj and not token_obj.is_expired():
        return JSONResponse(content={"detail": "logged in succesfully", "token": token_obj.token})
    
    if token_obj:
        db.delete(token_obj)
        db.commit()
        
    token_obj = TokenModel(user_id=user_obj.id, token = generate_token())
    db.add(token_obj)
    db.commit()
    db.refresh(token_obj)
    return JSONResponse(content={"detail" : "logged in succesfully", "token" : token_obj.token})


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