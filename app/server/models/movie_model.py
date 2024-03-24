from pydantic import BaseModel, field_validator
from server.utils.validators import release_date_validator


class AddMovie(BaseModel):
    title: str
    summery: str
    release_date: int
    director: str
    genres: list[str]
    actors: list[str]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "movie title",
                "summery": "what happened in the movie",
                "release_date": 2024,
                "director": "director name",
                "genres": ["drama", "comedy"],
                "actors": ["actor name", "actor name2"],
            }
        }

    @field_validator("release_date")
    def release_date_check(cls, value):
        return release_date_validator(int(value))

    class Settings:
        name = "add movie"
