from pydantic import BaseModel, EmailStr


class UserSignUp(BaseModel):
    username: str
    password: str
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Firstname Lastname",
                "email": "emmail@somwhere.somthing",
                "password": "3xt3m#",
            }
        }

    class Settings:
        name = "user"
