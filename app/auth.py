import hashlib
from jose import jwt
from datetime import datetime, timedelta


SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"


def hash_password(password: str):

    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password, hashed_password):

    return hash_password(plain_password) == hashed_password


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=1)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


def create_access_token(data: dict):

    to_encode = data.copy()

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token