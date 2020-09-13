import re


def valid_email(email: str, /):
    match = re.match(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        email)
    if match:
        return email
    else:
        raise ValueError("Not a valid email!")
