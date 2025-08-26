# core/auth/jwt_cookie_auth.py
from datetime import datetime, timezone
from typing import Final

import jwt
from fastapi import Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from core.config import settings
from core.db import get_db
from users.models import UserModel


def _decode_and_validate(token: str, expected_type: str) -> dict:
    # decode & validation (type & exp) JWT
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    if decoded.get("type") != expected_type:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    exp = decoded.get("exp")
    if exp is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    # compare TZ-aware
    if datetime.now(timezone.utc) > datetime.fromtimestamp(exp, tz=timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

    return decoded


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    # set both cookies (scure & HttpOnly)
    response.set_cookie(
        key=settings.COOKIE_ACCESS_NAME,
        value=access_token,
        max_age=settings.ACCESS_MAX_AGE,
        httponly=True,
        secure=False,   # True in Production
        samesite="lax", # If you have a separate domain, "none" may be required (with secure=True)
        path="/",)
    
    response.set_cookie(
        key=settings.COOKIE_REFRESH_NAME,
        value=refresh_token,
        max_age=settings.REFRESH_MAX_AGE,
        httponly=True,
        secure=False,   # True in Production
        samesite="lax",
        path="/",)


def set_access_cookie(response: Response, access_token: str) -> None:
    # update cookie access
    response.set_cookie(
        key=settings.COOKIE_ACCESS_NAME,
        value=access_token,
        max_age=settings.ACCESS_MAX_AGE,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
    )


def clear_auth_cookies(response: Response) -> None:
    # clear cookies (logout)
    response.delete_cookie(settings.COOKIE_ACCESS_NAME, path="/")
    response.delete_cookie(settings.COOKIE_REFRESH_NAME, path="/")


def get_current_user_from_cookies(request: Request, db: Session = Depends(get_db),) -> UserModel:
    # Dependency reads the access cookie for protected routes
    token = request.cookies.get(settings.COOKIE_ACCESS_NAME)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token cookie")

    decoded = _decode_and_validate(token, expected_type="access")
    user_id = decoded.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = db.query(UserModel).filter(UserModel.id == user_id).one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def get_user_id_from_refresh_cookie(request: Request) -> int:
    # For refresh: Returns only the user_id from the refresh token in the cookie.
    token = request.cookies.get(settings.COOKIE_REFRESH_NAME)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token cookie")

    decoded = _decode_and_validate(token, expected_type="refresh")
    user_id = decoded.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    return user_id