from fastapi import APIRouter, Response, status
from server.database.database import db
from server.models.user import UserSignUp
from server.schemas import user_schemas
from server.utils.hasher import password_generator

router = APIRouter()

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign-up/")
async def sign_up(user: UserSignUp, response: Response):
    user: dict = dict(user)
    user_exist: None | dict = db.users.find_one(
        {"$or": [{"username": user["username"]}, {"email": user["email"]}]}
    )
    if user_exist:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"response": "user with entered info already exists"}
    else:
        hashed_password: dict = password_generator(user["password"])
        user["password"] = hashed_password["password"]
        user["salt"] = hashed_password["salt"]
        db.users.insert_one(user)
        response.status_code = status.HTTP_201_CREATED
        return user_schemas.user_serializer(user)
