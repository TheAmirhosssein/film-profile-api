from typing import Dict, Optional


def user_serializer(user: Optional[Dict[str, str]]) -> Dict[str, str]:
    if user is None:
        return {}
    return {
        "username": user["username"],
        "email": user["email"],
        "fullname": user["fullname"],
    }
