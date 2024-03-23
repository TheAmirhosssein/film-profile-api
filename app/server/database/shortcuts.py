from server.database.database import db


async def is_available(
    new_value: str, old_value: str, collection: str, property_name: str
) -> bool:
    document = db[collection].find_one(
        {
            "$and": [
                {property_name: {"$ne": old_value}},
                {property_name: new_value},
            ]
        }
    )
    return document is None
