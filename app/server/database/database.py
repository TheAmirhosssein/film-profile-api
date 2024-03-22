from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")


client = MongoClient(config["MONGODB_URI"], config["MONGODB_PORT"])
db = client["movies"]
