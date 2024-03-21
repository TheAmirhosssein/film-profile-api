from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def main():
    return "hello world"
