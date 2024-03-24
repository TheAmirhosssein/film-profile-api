from fastapi import APIRouter, Depends, HTTPException, status
from server.database.database import db
from server.models import movie_model
from server.schemas.movie_schema import movie_serializer
from server.utils.jwt import JWTBearer

router = APIRouter(prefix="/movie", tags=["movie"])


@router.post("/add-movie/", summary="add movies")
async def add_movie(movie: movie_model.AddMovie, user=Depends(JWTBearer())):
    movie = dict(movie)
    movie["user_id"] = user["_id"]
    movie_exist = db.movies.find(
        {
            "$and": [
                {"title": movie["title"]},
                {"director": movie["director"].lower()},
            ]
        }
    )
    if movie_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie with same info is exists",
        )
    db.movies.insert_one(movie)
    return movie_serializer(movie)
