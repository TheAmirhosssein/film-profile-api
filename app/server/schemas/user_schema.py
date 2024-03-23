def user_serializer(user: any) -> dict:
    return {
        "username": user["username"],
        "email": user["email"],
        "fullname": user["fullname"],
    }
