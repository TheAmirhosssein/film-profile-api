import datetime
import re


def password_validator(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password must have at least 8 characters")
    if not any(c.isupper() for c in password):
        raise ValueError("Password must have at least one uppercase letter")
    if not any(c.islower() for c in password):
        raise ValueError("Password must have at least one lowercase letter")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must have at least one digit")
    if re.match("^[A-Za-z0-9]*$", password):
        raise ValueError("Password must have at least one symbol")
    if password == "Password@1234":
        raise ValueError("This password is not allowed")
    return password


def release_date_validator(year: str) -> str:
    date = datetime.date.today()
    current_year = int(date.strftime("%Y"))
    FIRST_RELEASE_DATE = 1895
    if year > current_year:
        raise ValueError("the movie is not released yet")
    if year < FIRST_RELEASE_DATE:
        raise ValueError("the movie release year is too old")
    return year
