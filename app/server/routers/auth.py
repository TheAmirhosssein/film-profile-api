from fastapi import APIRouter, HTTPException, Response, status
from server.database.database import db
from app.server.models.user_model import UserLogin, UserSignUp
from app.server.schemas import user_schema
from server.utils import hasher, jwt

router = APIRouter()

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign-up/", summary="create new user")
async def sign_up(user: UserSignUp, response: Response):
    user: dict = dict(user)
    user_exist: None | dict = db.users.find_one(
        {"$or": [{"username": user["username"]}, {"email": user["email"]}]}
    )
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this information already exist",
        )
    else:
        hashed_password: dict = hasher.password_generator(user["password"])
        user["password"] = hashed_password["password"]
        user["salt"] = hashed_password["salt"]
        db.users.insert_one(user)
        response.status_code = status.HTTP_201_CREATED
        return user_schema.user_serializer(user)


@router.post("/login/", summary="create access and refresh tokens for user")
async def login(credential: UserLogin):
    credential = dict(credential)
    user = db.users.find_one({"username": credential["username"]})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    if not hasher.check_password(user["password"], credential["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    return {
        "access_token": jwt.create_refresh_token(user["username"]),
        "refresh_token": jwt.create_refresh_token(user["username"]),
    }
