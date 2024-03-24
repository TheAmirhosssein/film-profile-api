import math

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from server.database.database import db
from server.models import movie_model
from server.schemas.movie_schema import movie_serializer, movies_serializer
from server.utils.jwt import JWTBearer

router = APIRouter(prefix="/movie", tags=["movie"])


@router.post("/add-movie/", summary="add movies")
async def add_movie(movie_json: movie_model.AddMovie, user=Depends(JWTBearer())):
    movie: dict = dict(movie_json)
    movie["user_id"] = user["_id"]
    movie_exist = db.movies.find_one(
        {
            "$and": [
                {"title": movie["title"]},
                {"director": movie["director"].lower()},
            ]
        }
    )
    if movie_exist is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie with same info is exists",
        )
    insert_result = db.movies.insert_one(movie)
    created_movie = db.movies.find_one({"_id": insert_result.inserted_id})
    return movie_serializer(created_movie)


@router.get("/movies/", summary="movies list")
async def movies_list(page: int = 1, size: int = 10):
    pages_count: int = math.ceil(db.movies.count_documents({}) / size)
    movies = db.movies.find().skip((page - 1) * size).limit(size)
    serialized_movies = movies_serializer(movies)
    return {"page_count": pages_count, "result": serialized_movies}


@router.get("/movies/{object_id}", summary="movie detail")
async def movie_detail(object_id: str):
    movie = db.movies.find_one({"_id": ObjectId(object_id)})
    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="movie not found"
        )
    serialized_movies = movie_serializer(movie)
    return serialized_movies
