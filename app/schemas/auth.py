# app/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re

from app.core.settings import settings


class UserRegister(BaseModel):
    username: str = Field(..., min_length=settings.username_min_length, max_length=settings.username_max_length)
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=settings.password_min_length, max_length=settings.password_max_length)
    confirm_password: str

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Les mots de passe ne correspondent pas')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PasswordReset(BaseModel):
    password: str = Field(..., min_length=settings.password_min_length, max_length=settings.password_max_length)
    confirm_password: str
    password_token: str

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Les mots de passe ne correspondent pas')
        return v


class ForgottenPassword(BaseModel):
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
