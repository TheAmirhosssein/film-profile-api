from pymongo.cursor import Cursor
from typing import Optional, Dict


def movie_serializer(movie: Optional[Dict[str, str]]) -> Dict[str, str]:
    if movie is None:
        return {}
    return {
        "id": str(movie["_id"]),
        "title": movie["title"],
        "summery": movie["summery"],
        "release_date": movie["release_date"],
        "director": movie["director"],
        "genres": movie["genres"],
        "actors": movie["actors"],
    }


def movies_serializer(movies: Cursor) -> list[dict]:
    movies_list = [movie_serializer(movie) for movie in movies]
    return movies_list
