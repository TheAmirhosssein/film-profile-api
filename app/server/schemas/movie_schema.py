from typing import Dict, Optional

from bson import ObjectId
from pymongo.cursor import Cursor
from server.database.database import db
from server.schemas.user_schema import user_serializer


def movie_serializer(
    movie: Optional[Dict[str, str]],
) -> Dict[str, str | Dict[str, str] | list]:
    if movie is None:
        return {}
    user_id: str = str(movie["user_id"])
    movie_user: Optional[Dict[str, str]] = db.users.find_one({"_id": ObjectId(user_id)})
    user = user_serializer(movie_user)
    watched_by = [
        user_serializer(db.users.find_one({"_id": ObjectId(watched_user)}))
        for watched_user in movie.get("watched_by", [])
    ]
    return {
        "id": str(movie["_id"]),
        "title": movie["title"],
        "summery": movie["summery"],
        "release_date": movie["release_date"],
        "director": movie["director"],
        "genres": movie["genres"],
        "actors": movie["actors"],
        "created_by": user,
        "watched_by": watched_by,
    }


def movies_serializer(movies: Cursor) -> list[dict]:
    movies_list = [movie_serializer(movie) for movie in movies]
    return movies_list
