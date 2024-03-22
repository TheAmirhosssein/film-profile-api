from pydantic import BaseModel, EmailStr


class UserSignUp(BaseModel):
    username: str
    password: str
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "username": "cool_username",
                "email": "emmail@somwhere.somthing",
                "password": "3xt3m#",
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
                "password": "3xt3m#",
            }
        }

    class Settings:
        name = "user_login"
