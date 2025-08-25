# core/users/schemas.py
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class UserLoginSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=250, description="this is usename")
    password: str = Field(..., description="user's password")


class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=250, description="this is usename")
    password: str = Field(..., description="user's password")
    password_confirm: str = Field(..., description="confirm user's password")
    
    @field_validator("password_confirm")
    def check_password_match(cls, password_confirm, validation):
        if not password_confirm == validation.data.get("password"):
            raise ValueError("password doesnt match!")
        return password_confirm
        
    