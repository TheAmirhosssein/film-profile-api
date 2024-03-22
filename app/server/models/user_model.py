import re

from pydantic import BaseModel, EmailStr, field_validator
from fastapi import Body


class UserSignUp(BaseModel):
    username: str = Body(min_length=6, regex="^[a-zA-Z0-9_]*$", max_length=30)
    password: str
    email: EmailStr

    @field_validator("password")
    def check_password(cls, value):
        value = str(value)
        if len(value) < 8:
            raise ValueError("Password must have at least 8 characters")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must have at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must have at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must have at least one digit")
        if re.match("^[A-Za-z0-9]*$", value):
            raise ValueError("Password must have at least one symbol")
        if value == "Password@1234":
            raise ValueError("This password is not allowed")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "username": "cool_username",
                "email": "emmail@somwhere.somthing",
                "password": "Password@1234",
            }
        }

    class Settings:
        name = "user_sign_up"


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "cool_username",
                "password": "Password@1234",
            }
        }

    class Settings:
        name = "user_login"
