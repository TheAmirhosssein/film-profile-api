import bcrypt


def password_generator(password: str) -> dict[str:str, str:str]:
    bytes_password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes_password, salt)
    result = {"password": hashed_password, "salt": salt}
    return result


def check_password(user_password: str, password: str) -> bool:
    bytes_password = password.encode("utf-8")
    result = bcrypt.checkpw(bytes_password, user_password)
    return result
