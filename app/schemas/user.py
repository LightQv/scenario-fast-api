from pydantic import BaseModel, field_validator, Field, ConfigDict
from typing import Optional
from uuid import UUID

from app.schemas.validation_types import ValidPassword, ValidEmail


class UserBase(BaseModel):
    username: str = Field(..., min_length=5, max_length=100)
    email: ValidEmail = Field(..., max_length=255)


class UserCreate(UserBase):
    password: str = Field(..., min_length=7, max_length=30)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=5, max_length=100)
    email: Optional[ValidEmail] = Field(None, max_length=255)
    password: Optional[ValidPassword] = Field(None, min_length=7, max_length=30)


class UserUpdateEmail(BaseModel):
    email: ValidEmail = Field(..., max_length=255)


class UserUpdatePassword(BaseModel):
    password: ValidPassword = Field(..., min_length=7, max_length=30)
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
    id: UUID
    username: str
    email: str
    profile_banner: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True
    )


class UserPublic(BaseModel):
    username: str
    email: str
    profile_banner: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True
    )


class UserBanner(BaseModel):
    profile_banner: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True
    )