def movie_serializer(movie: any) -> dict:
    return {
        "title": movie["title"],
        "summery": movie["summery"],
        "release_date": movie["release_date"],
        "director": movie["director"],
        "genres": movie["genres"],
        "actors": movie["actors"],
    }
