def user_serializer(user: dict) -> dict:
    return {
        "username": user["username"],
        "email": user["email"],
        "fullname": user["fullname"],
    }
