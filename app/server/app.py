from fastapi import FastAPI
from server.routers import movie, auth

app = FastAPI()
app.include_router(auth.router, prefix="/api/v1")
app.include_router(movie.router, prefix="/api/v1")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
