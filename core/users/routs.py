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

# Token Authenticated
"""
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
"""


# ---------- JWT ----------

from auth.jwt_auth import generate_access_token, generate_refresh_token, decode_refresh_token

@router.post("/login")
async def user_login(payload: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(username=payload.username.lower()).first()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username doesnt exists!")
    if not user_obj.verify_password(payload.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password is invalid!")
    
    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)
    
    return JSONResponse(content={"detail" : "logged in succesfully",
                                 "access token" : access_token,
                                 "refresh token" : refresh_token,
                                 })


@router.post("/register")
async def user_register(payload: UserRegisterSchema, db: Session = Depends(get_db)):
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


@router.post("/refresh-token")
async def user_refresh_token(payload: UserRefreshTokenSchema, db: Session = Depends(get_db)):
    user_id = decode_refresh_token(payload.token)
    
    access_token = generate_access_token(user_id)

    return JSONResponse(content={"access token":access_token})



# ---------- JWT Cookie ----------
from auth.jwt_cookie_auth import (
    set_auth_cookies,
    set_access_cookie,
    clear_auth_cookies,
    get_current_user_from_cookies,
    get_user_id_from_refresh_cookie,
)
from fastapi import Request


@router.post("/login-cookie")
def user_login_cookie(payload: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(username=payload.username.lower()).first()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username doesnt exists!")
    if not user_obj.verify_password(payload.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password is invalid!")

    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)

    # set cookies on response
    resp = JSONResponse(content={"detail": "logged in successfully (cookie auth)"})
    set_auth_cookies(resp, access_token, refresh_token)
    return resp


@router.post("/refresh-cookie")
def user_refresh_cookie(request: Request):
    # Reads the refresh token from the cookie, creates a new access token if it is valid, and only updates the access cookie.
    user_id = get_user_id_from_refresh_cookie(request)
    new_access = generate_access_token(user_id)

    resp = JSONResponse(content={"detail": "access token refreshed (cookie auth)"})
    set_access_cookie(resp, new_access)
    return resp


@router.post("/logout-cookie")
def user_logout_cookie():
    # clear cookies (logout)
    resp = JSONResponse(content={"detail": "logged out (cookie auth)"})
    clear_auth_cookies(resp)
    return resp


# Example of a cookie-protected rout (instead of Bearer)
@router.get("/me-cookie")
def me_cookie(user: UserModel = Depends(get_current_user_from_cookies)):
    return {"id": user.id, "username": user.username}