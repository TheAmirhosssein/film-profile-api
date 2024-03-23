from pydantic import BaseModel, EmailStr, field_validator
from fastapi import Body
from server.utils.validators import password_validator


class UserSignUp(BaseModel):
    username: str = Body(min_length=6, regex="^[a-zA-Z0-9_]*$", max_length=30)
    fullname: str = Body(max_length=100)
    password: str
    email: EmailStr

    @field_validator("password")
    def check_password(cls, value):
        return password_validator(str(value))

    class Config:
        json_schema_extra = {
            "example": {
                "username": "cool_username",
                "email": "emmail@somwhere.somthing",
                "fullname": "firstname lastname",
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


class RefreshToken(BaseModel):
    refresh_token: str

    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "refresh_token",
            }
        }

    class Settings:
        name = "refresh_token"


class UserUpdate(BaseModel):
    username: str = Body(min_length=6, regex="^[a-zA-Z0-9_]*$", max_length=30)
    fullname: str = Body(max_length=100)
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "username": "cool_username",
                "email": "emmail@somwhere.somthing",
                "fullname": "firstname lastname",
            }
        }

    class Settings:
        name = "user update"


class ChangePassword(BaseModel):
    password: str
    new_password: str
    new_password2: str

    @field_validator("new_password")
    def check_password(cls, value):
        return password_validator(str(value))
