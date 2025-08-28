from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from uuid import UUID


class UserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=100)
    email: EmailStr = Field(..., max_length=255)


class UserCreate(UserBase):
    password: str = Field(..., min_length=7, max_length=30)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=5, max_length=100)
    email: Optional[EmailStr] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=7, max_length=30)


class UserUpdateEmail(BaseModel):
    email: EmailStr = Field(..., max_length=255)


class UserUpdatePassword(BaseModel):
    password: str = Field(..., min_length=7, max_length=30)
    confirm_password: str

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Les mots de passe ne correspondent pas')
        return v


class UserUpdateBanner(BaseModel):
    banner_link: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: str
    profile_banner: Optional[str] = None


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str
    profile_banner: Optional[str] = None


class UserBanner(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    profile_banner: Optional[str] = None
