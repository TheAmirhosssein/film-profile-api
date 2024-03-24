from fastapi import APIRouter, Depends
from server.database.database import db
from server.models import movie_model
from server.schemas.movie_schema import movie_serializer
from server.utils.jwt import JWTBearer

router = APIRouter(prefix="/movie", tags=["movie"])


@router.post("/add-movie/", summary="add movies")
async def add_movie(movie: movie_model.AddMovie, user=Depends(JWTBearer())):
    movie = dict(movie)
    movie["created_user"] = user
    db.movies.insert_one(movie)
    return movie_serializer(movie)
